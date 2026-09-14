//! `caas`: a command-line client for the Catharsis as a Service content API.

use std::env;
use std::path::PathBuf;
use std::process::ExitCode;

use caas_content::Library;

const USAGE: &str = "usage: caas [--api <dir>] [--lang <code>] <command>

commands:
  advice list              list advice entries with their evidence grade
  advice show <slug>       show one advice entry with its practice steps
  research list            list research notes
  check                    verify the integrity of the exported library (exit 1 on problems)
  endpoint                 print the POST /v1/catharsis response

The API directory defaults to $CAAS_API_DIR, then public/api/v1.
The language defaults to the site's default language.";

struct Options {
    api: PathBuf,
    language: Option<String>,
    words: Vec<String>,
    help: bool,
}

fn parse(args: &[String]) -> Result<Options, String> {
    let mut options = Options {
        api: env::var_os("CAAS_API_DIR")
            .map_or_else(|| PathBuf::from("public/api/v1"), PathBuf::from),
        language: None,
        words: Vec::new(),
        help: false,
    };
    let mut iter = args.iter();
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--api" => {
                let dir = iter
                    .next()
                    .ok_or_else(|| "--api needs a directory".to_owned())?;
                options.api = PathBuf::from(dir);
            }
            "--lang" => {
                let code = iter
                    .next()
                    .ok_or_else(|| "--lang needs a language code".to_owned())?;
                options.language = Some(code.clone());
            }
            "-h" | "--help" => options.help = true,
            _ => options.words.push(arg.clone()),
        }
    }
    Ok(options)
}

fn run(args: &[String]) -> Result<ExitCode, String> {
    let options = parse(args)?;
    if options.help {
        println!("{USAGE}");
        return Ok(ExitCode::SUCCESS);
    }
    if options.words.is_empty() {
        return Err("no command given".to_owned());
    }

    let library = Library::load(&options.api).map_err(|error| {
        format!(
            "cannot load the API from {}: {error}",
            options.api.display()
        )
    })?;
    let language = options
        .language
        .as_deref()
        .unwrap_or(library.index.default_language.as_str());
    if !library.index.languages.iter().any(|code| code == language) {
        return Err(format!(
            "unknown language {language} (available: {})",
            library.index.languages.join(", ")
        ));
    }

    let words: Vec<&str> = options.words.iter().map(String::as_str).collect();
    match words.as_slice() {
        ["advice", "list"] => {
            for entry in library.advice(language) {
                println!(
                    "{:<30} {:<24} {}",
                    entry.slug, entry.evidence_grade, entry.title
                );
            }
            Ok(ExitCode::SUCCESS)
        }
        ["advice", "show", slug] => {
            let entry = library
                .find_advice(language, slug)
                .ok_or_else(|| format!("no advice entry {slug} in {language}"))?;
            println!("{}", entry.title);
            println!("{} · {}", entry.kicker, entry.evidence_label);
            println!();
            println!("{}", entry.recommendation);
            println!();
            for (number, step) in entry.practice.iter().enumerate() {
                println!("{:>2}. {step}", number + 1);
            }
            println!();
            println!("{}", entry.url);
            Ok(ExitCode::SUCCESS)
        }
        ["research", "list"] => {
            for note in library.research(language) {
                println!("{:<30} {}", note.slug, note.title);
            }
            Ok(ExitCode::SUCCESS)
        }
        ["check"] => {
            let problems = library.problems();
            if problems.is_empty() {
                println!(
                    "library ok: {} languages, {} research notes, {} advice entries, {} references, {} commands",
                    library.index.languages.len(),
                    library.research(language).len(),
                    library.advice(language).len(),
                    library.references.len(),
                    library.commands.len()
                );
                Ok(ExitCode::SUCCESS)
            } else {
                for problem in &problems {
                    eprintln!("problem: {problem}");
                }
                Ok(ExitCode::from(1))
            }
        }
        ["endpoint"] => {
            let endpoint = &library.index.endpoint;
            let response = serde_json::json!({
                "request": format!("{} {}", endpoint.method, endpoint.path),
                "status": endpoint.status,
                "relief": "temporary",
                "problem_solved": endpoint.problem_solved,
            });
            let text =
                serde_json::to_string_pretty(&response).map_err(|error| error.to_string())?;
            println!("{text}");
            Ok(ExitCode::SUCCESS)
        }
        _ => Err(format!("unknown command: {}", words.join(" "))),
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().skip(1).collect();
    match run(&args) {
        Ok(code) => code,
        Err(message) => {
            eprintln!("caas: {message}\n\n{USAGE}");
            ExitCode::from(2)
        }
    }
}
