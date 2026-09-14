//! Contract tests against the real export produced by `scripts/export-api.py`.
//!
//! Set `CAAS_API_DIR` to an absolute `api/v1` directory to test a specific export; otherwise the
//! tests run the exporter into a temporary directory.

use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::OnceLock;

use caas_content::{ClaimType, EvidenceGrade, EvidenceLevel, Library};

fn api_dir() -> &'static Path {
    static DIR: OnceLock<PathBuf> = OnceLock::new();
    DIR.get_or_init(|| {
        if let Some(dir) = std::env::var_os("CAAS_API_DIR") {
            return PathBuf::from(dir);
        }
        let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let out =
            std::env::temp_dir().join(format!("caas-content-contract-{}", std::process::id()));
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

fn library() -> Library {
    Library::load(api_dir()).expect("the exported library loads")
}

#[test]
fn every_language_has_research_and_advice() {
    let library = library();
    assert!(!library.index.languages.is_empty());
    for language in &library.index.languages {
        assert!(
            !library.research(language).is_empty(),
            "no research notes in {language}"
        );
        assert!(
            !library.advice(language).is_empty(),
            "no advice entries in {language}"
        );
    }
}

#[test]
fn the_exported_library_has_no_integrity_problems() {
    let problems = library().problems();
    assert!(
        problems.is_empty(),
        "integrity problems:\n{}",
        problems.join("\n")
    );
}

#[test]
fn urls_live_under_the_site() {
    let library = library();
    for language in &library.index.languages {
        for note in library.research(language) {
            assert!(
                note.url.starts_with(&library.index.site),
                "{} is outside {}",
                note.url,
                library.index.site
            );
        }
        for entry in library.advice(language) {
            assert!(
                entry.url.starts_with(&library.index.site),
                "{} is outside {}",
                entry.url,
                library.index.site
            );
        }
    }
}

#[test]
fn the_endpoint_succeeds_without_solving_the_problem() {
    let endpoint = library().index.endpoint;
    assert_eq!(endpoint.method, "POST");
    assert_eq!(endpoint.path, "/v1/catharsis");
    assert_eq!(endpoint.status, 200);
    assert!(!endpoint.problem_solved);
}

#[test]
fn advice_with_the_strongest_grade_exists() {
    let library = library();
    let default = library.index.default_language.clone();
    assert!(
        library
            .advice(&default)
            .iter()
            .any(|entry| entry.evidence_grade == EvidenceGrade::MetaAnalytic)
    );
}

#[test]
fn the_ledger_covers_every_claim_type_and_grades_within_its_sources() {
    let library = library();
    assert!(!library.claims.is_empty());
    assert_eq!(library.sources.len(), library.references.len());
    for kind in [
        ClaimType::Empirical,
        ClaimType::ClinicalBoundary,
        ClaimType::Artistic,
    ] {
        assert!(
            library.claims.iter().any(|claim| claim.claim_type == kind),
            "no {kind} claim"
        );
    }
    for claim in &library.claims {
        assert!(claim.review_due > claim.last_reviewed, "{}", claim.id);
        if claim.sources.is_empty() {
            assert_eq!(claim.evidence_level, EvidenceLevel::E, "{}", claim.id);
        }
    }
    assert!(library.term("catharsis").is_some());
    assert!(!library.changelog.is_empty());
}

#[test]
fn every_registered_command_names_a_verification() {
    let library = library();
    assert!(!library.commands.is_empty());
    for command in &library.commands {
        assert!(
            !command.verified_by.is_empty(),
            "{} has no verification",
            command.id
        );
    }
}
