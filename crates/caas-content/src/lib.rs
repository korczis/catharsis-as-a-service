//! Typed access to the Catharsis as a Service content API.
//!
//! The site exports its research notes, advice entries, references and command registry as
//! versioned JSON under `api/v1` (written by `scripts/export-api.py`). This crate is the Rust side
//! of that contract: it deserializes the files and checks the invariants other applications rely on.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::fs;
use std::path::{Path, PathBuf};

use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};

/// The API version this crate understands.
pub const API_VERSION: u32 = 1;

/// `api/v1/index.json`: the entry point that names every other file.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ApiIndex {
    pub api_version: u32,
    pub site: String,
    pub default_language: String,
    pub languages: Vec<String>,
    pub collections: Collections,
    pub references: String,
    pub commands: String,
    pub endpoint: Endpoint,
}

/// File names of the per-language collections, keyed by language code.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Collections {
    pub research: BTreeMap<String, String>,
    pub advice: BTreeMap<String, String>,
}

/// The artifact's endpoint: it succeeds, and the problem stays unsolved.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Endpoint {
    pub method: String,
    pub path: String,
    pub status: u16,
    pub problem_solved: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ResearchNote {
    pub slug: String,
    pub url: String,
    pub title: String,
    pub description: String,
    pub date: String,
    pub kicker: String,
    pub summary: String,
    pub key_points: Vec<String>,
    pub tags: Vec<String>,
    pub references: Vec<String>,
}

/// How strong the evidence behind an advice entry is, strongest first.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum EvidenceGrade {
    MetaAnalytic,
    ReplicatedExperimental,
    Experimental,
    Observational,
    Theoretical,
}

impl EvidenceGrade {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::MetaAnalytic => "meta-analytic",
            Self::ReplicatedExperimental => "replicated-experimental",
            Self::Experimental => "experimental",
            Self::Observational => "observational",
            Self::Theoretical => "theoretical",
        }
    }
}

impl fmt::Display for EvidenceGrade {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.pad(self.as_str())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdviceEntry {
    pub slug: String,
    pub url: String,
    pub title: String,
    pub description: String,
    pub kicker: String,
    pub evidence_grade: EvidenceGrade,
    pub evidence_label: String,
    pub recommendation: String,
    pub practice: Vec<String>,
    pub limits: Vec<String>,
    /// Slugs of research notes in the same language.
    pub related: Vec<String>,
    pub tags: Vec<String>,
    pub references: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Reference {
    pub kind: String,
    pub authors: String,
    pub year: String,
    pub title: String,
    pub container: String,
    pub volume: String,
    pub issue: String,
    pub pages: String,
    pub publisher: String,
    pub doi: String,
    pub url: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub title_cs: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub year_cs: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Command {
    pub id: String,
    pub group: String,
    pub command: String,
    pub summary: BTreeMap<String, String>,
    pub source: String,
    pub verified_by: Vec<String>,
}

#[derive(Debug)]
pub enum Error {
    Read {
        path: PathBuf,
        source: std::io::Error,
    },
    Parse {
        path: PathBuf,
        source: serde_json::Error,
    },
    UnsupportedVersion {
        found: u32,
    },
    MissingCollection {
        collection: &'static str,
        language: String,
    },
}

impl fmt::Display for Error {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Read { path, source } => {
                write!(formatter, "cannot read {}: {source}", path.display())
            }
            Self::Parse { path, source } => {
                write!(formatter, "cannot parse {}: {source}", path.display())
            }
            Self::UnsupportedVersion { found } => {
                write!(
                    formatter,
                    "api version {found} is not supported (expected {API_VERSION})"
                )
            }
            Self::MissingCollection {
                collection,
                language,
            } => {
                write!(
                    formatter,
                    "index.json names no {collection} collection for {language}"
                )
            }
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Read { source, .. } => Some(source),
            Self::Parse { source, .. } => Some(source),
            Self::UnsupportedVersion { .. } | Self::MissingCollection { .. } => None,
        }
    }
}

/// The whole exported library, loaded from an `api/v1` directory.
#[derive(Debug, Clone)]
pub struct Library {
    pub index: ApiIndex,
    pub research: BTreeMap<String, Vec<ResearchNote>>,
    pub advice: BTreeMap<String, Vec<AdviceEntry>>,
    pub references: BTreeMap<String, Reference>,
    pub commands: Vec<Command>,
}

fn read_json<T: DeserializeOwned>(path: &Path) -> Result<T, Error> {
    let text = fs::read_to_string(path).map_err(|source| Error::Read {
        path: path.to_path_buf(),
        source,
    })?;
    serde_json::from_str(&text).map_err(|source| Error::Parse {
        path: path.to_path_buf(),
        source,
    })
}

impl Library {
    /// Loads `index.json` and every file it names from `dir`.
    pub fn load(dir: impl AsRef<Path>) -> Result<Self, Error> {
        let dir = dir.as_ref();
        let index: ApiIndex = read_json(&dir.join("index.json"))?;
        if index.api_version != API_VERSION {
            return Err(Error::UnsupportedVersion {
                found: index.api_version,
            });
        }

        let mut research = BTreeMap::new();
        let mut advice = BTreeMap::new();
        for language in &index.languages {
            let file = index.collections.research.get(language).ok_or_else(|| {
                Error::MissingCollection {
                    collection: "research",
                    language: language.clone(),
                }
            })?;
            research.insert(language.clone(), read_json(&dir.join(file))?);

            let file =
                index
                    .collections
                    .advice
                    .get(language)
                    .ok_or_else(|| Error::MissingCollection {
                        collection: "advice",
                        language: language.clone(),
                    })?;
            advice.insert(language.clone(), read_json(&dir.join(file))?);
        }

        let references = read_json(&dir.join(&index.references))?;
        let commands = read_json(&dir.join(&index.commands))?;
        Ok(Self {
            index,
            research,
            advice,
            references,
            commands,
        })
    }

    pub fn research(&self, language: &str) -> &[ResearchNote] {
        self.research
            .get(language)
            .map(Vec::as_slice)
            .unwrap_or(&[])
    }

    pub fn advice(&self, language: &str) -> &[AdviceEntry] {
        self.advice.get(language).map(Vec::as_slice).unwrap_or(&[])
    }

    pub fn find_advice(&self, language: &str, slug: &str) -> Option<&AdviceEntry> {
        self.advice(language)
            .iter()
            .find(|entry| entry.slug == slug)
    }

    /// Integrity problems an application should refuse to run with. Empty when the library is sound.
    pub fn problems(&self) -> Vec<String> {
        let mut problems = Vec::new();
        let default = self.index.default_language.as_str();
        let research_slugs: BTreeSet<&str> = self
            .research(default)
            .iter()
            .map(|note| note.slug.as_str())
            .collect();
        let advice_slugs: BTreeSet<&str> = self
            .advice(default)
            .iter()
            .map(|entry| entry.slug.as_str())
            .collect();

        if !self
            .index
            .languages
            .iter()
            .any(|language| language == default)
        {
            problems.push(format!(
                "default language {default} is not in the language list"
            ));
        }
        if self.index.endpoint.status != 200 || self.index.endpoint.problem_solved {
            problems.push(
                "endpoint contract changed: expected status 200 with problem_solved false"
                    .to_owned(),
            );
        }

        for language in &self.index.languages {
            let slugs: BTreeSet<&str> = self
                .research(language)
                .iter()
                .map(|note| note.slug.as_str())
                .collect();
            if slugs != research_slugs {
                problems.push(format!(
                    "research notes in {language} differ from {default}"
                ));
            }
            let slugs: BTreeSet<&str> = self
                .advice(language)
                .iter()
                .map(|entry| entry.slug.as_str())
                .collect();
            if slugs != advice_slugs {
                problems.push(format!(
                    "advice entries in {language} differ from {default}"
                ));
            }

            for note in self.research(language) {
                if note.references.is_empty() {
                    problems.push(format!(
                        "research/{language}/{}: cites no references",
                        note.slug
                    ));
                }
                for id in &note.references {
                    if !self.references.contains_key(id) {
                        problems.push(format!(
                            "research/{language}/{}: unknown reference {id}",
                            note.slug
                        ));
                    }
                }
            }

            for entry in self.advice(language) {
                if entry.practice.len() < 3 {
                    problems.push(format!(
                        "advice/{language}/{}: fewer than 3 practice steps",
                        entry.slug
                    ));
                }
                if entry.references.is_empty() {
                    problems.push(format!(
                        "advice/{language}/{}: cites no references",
                        entry.slug
                    ));
                }
                for id in &entry.references {
                    if !self.references.contains_key(id) {
                        problems.push(format!(
                            "advice/{language}/{}: unknown reference {id}",
                            entry.slug
                        ));
                    }
                }
                for related in &entry.related {
                    if !research_slugs.contains(related.as_str()) {
                        problems.push(format!(
                            "advice/{language}/{}: related research note {related} does not exist",
                            entry.slug
                        ));
                    }
                }
            }
        }
        problems
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn evidence_grades_use_the_exported_spelling() {
        let grade: EvidenceGrade =
            serde_json::from_str("\"replicated-experimental\"").expect("grade parses");
        assert_eq!(grade, EvidenceGrade::ReplicatedExperimental);
        assert_eq!(
            serde_json::to_string(&EvidenceGrade::MetaAnalytic).expect("grade serializes"),
            "\"meta-analytic\""
        );
        assert_eq!(
            format!("{:<15}|", EvidenceGrade::Theoretical),
            "theoretical    |"
        );
    }

    #[test]
    fn grades_order_from_strongest_to_weakest() {
        assert!(EvidenceGrade::MetaAnalytic < EvidenceGrade::Theoretical);
    }

    #[test]
    fn loading_a_missing_directory_reports_the_path() {
        let error = Library::load("does/not/exist").expect_err("missing directory fails");
        assert!(matches!(error, Error::Read { .. }));
        assert!(error.to_string().contains("index.json"));
    }
}
