+++
title = "Commands"
description = "Every command mentioned on this site, in the README and in the documentation: what it does, where it lives and which test or CI job verifies it."
template = "commands.html"
+++

This registry lists every command that appears anywhere in this project's documentation. Each entry links to its source file and names the tests or CI jobs that execute it.

The registry is enforced. A documentation page that mentions a command missing from this list, or mentions a command in prose without linking to its entry here, fails validation. A registry entry whose verification is not backed by an existing test or CI job fails the test suite.
