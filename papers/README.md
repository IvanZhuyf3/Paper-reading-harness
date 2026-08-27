# Papers

Each paper uses an isolated workspace:

```text
papers/<paper_slug>/
├── README.md       # identity, provenance, and status
├── source/         # immutable paper and supplied source files
├── model/          # pending paper-model reconstruction
├── sessions/       # saved training/reading sessions
└── artifacts/      # extracted text, rendered pages, and other derived files
```

Do not edit files under `source/`. Generated models remain provisional until human approval and promotion into `curriculum/`.
