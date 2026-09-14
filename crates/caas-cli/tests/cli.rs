//! End-to-end tests of the `caas` binary against the real content export.

use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::OnceLock;

use caas_content::Library;

fn api_dir() -> &'static Path {
    static DIR: OnceLock<PathBuf> = OnceLock::new();
    DIR.get_or_init(|| {
        if let Some(dir) = std::env::var_os("CAAS_API_DIR") {
            return PathBuf::from(dir);
        }
        let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let out = std::env::temp_dir().join(format!("caas-cli-test-{}", std::process::id()));
        let status = Command::new("python3")
            .arg(root.join("scripts/export-api.py"))
            .arg("--out")
            .arg(&out)
            .status()
            .expect("python3 runs");
        assert!(status.success(), "scripts/export-api.py failed");
        out.join("api/v1")
    })
}

fn caas(args: &[&str]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_caas"))
        .arg("--api")
        .arg(api_dir())
        .args(args)
        .output()
        .expect("caas runs")
}

fn stdout(output: &Output) -> String {
    String::from_utf8(output.stdout.clone()).expect("utf-8 stdout")
}

#[test]
fn advice_list_prints_every_entry_with_its_grade() {
    let library = Library::load(api_dir()).expect("library loads");
    let output = caas(&["advice", "list"]);
    assert!(output.status.success());
    let text = stdout(&output);
    let default = library.index.default_language.clone();
    assert_eq!(text.lines().count(), library.advice(&default).len());
    for entry in library.advice(&default) {
        assert!(text.contains(&entry.slug), "{} is missing", entry.slug);
        assert!(text.contains(entry.evidence_grade.as_str()));
    }
}

#[test]
fn advice_show_prints_the_localized_entry() {
    let library = Library::load(api_dir()).expect("library loads");
    for language in &library.index.languages {
        let entry = &library.advice(language)[0];
        let output = caas(&["advice", "show", &entry.slug, "--lang", language]);
        assert!(output.status.success(), "advice show failed for {language}");
        let text = stdout(&output);
        assert!(text.contains(&entry.title));
        assert!(text.contains(&entry.recommendation));
        assert!(text.contains(" 1. "));
    }
}

#[test]
fn research_list_matches_the_library() {
    let library = Library::load(api_dir()).expect("library loads");
    let output = caas(&["research", "list", "--lang", "cs"]);
    assert!(output.status.success());
    assert_eq!(
        stdout(&output).lines().count(),
        library.research("cs").len()
    );
}

#[test]
fn check_passes_on_the_exported_library() {
    let output = caas(&["check"]);
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(stdout(&output).starts_with("library ok"));
}

#[test]
fn endpoint_reports_success_without_resolution() {
    let output = caas(&["endpoint"]);
    assert!(output.status.success());
    let response: serde_json::Value = serde_json::from_str(&stdout(&output)).expect("json");
    assert_eq!(response["status"], 200);
    assert_eq!(response["problem_solved"], false);
    assert_eq!(response["request"], "POST /v1/catharsis");
}

#[test]
fn unknown_commands_and_languages_are_usage_errors() {
    for args in [
        &["dance"][..],
        &["advice", "list", "--lang", "xx"][..],
        &[][..],
    ] {
        let output = caas(args);
        assert_eq!(output.status.code(), Some(2), "{args:?}");
        assert!(String::from_utf8_lossy(&output.stderr).contains("usage: caas"));
    }
}

#[test]
fn help_exits_successfully() {
    let output = caas(&["--help"]);
    assert!(output.status.success());
    assert!(stdout(&output).contains("advice show <slug>"));
}
