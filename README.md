# Zen Flesh, Zen Bones<!-- omit from toc -->

This repository holds code dedicated to extracting some knowledge graph out of the 1957 pdf version of Paul Reps' compilation
[Zen flesh, zen bones](./original_data/1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com.pdf).

## Table of contents<!-- omit from toc -->

- [Notes concerning the original book](#notes-concerning-the-original-book)
- [Running the PDF converter with python](#running-the-pdf-converter-with-python)
- [Running the PDF converter with docker](#running-the-pdf-converter-with-docker)
- [Running the PDF converter with jejune\_cli](#running-the-pdf-converter-with-jejune_cli)
- [Running the data workflow with jejune\_cli](#running-the-data-workflow-with-jejune_cli)

## Notes concerning the original book

This directory holds a copy of the 1957 pdf version of Paul Reps' compilation
[Zen flesh, zen bones](./original_data/1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com.pdf) as offered online by [OceanoPDF](https://oceanofpdf.com/authors/paul-reps/pdf-epub-zen-flesh-zen-bones-a-collection-of-zen-and-pre-zen-writings-download/).

### References

- [ISBN-13: 9780385081030](https://isbnsearch.org/isbn/9780385081030)
- [Wikipedia](https://en.wikipedia.org/wiki/Zen_Flesh,_Zen_Bones)

### Book peculiarities

- Within chapter `101 ZEN STORIES`,

  - there are two sub-chapters with number `46.`
  - there is no sub-chapter numbered `49.`

- Within chapter the `CENTERING` chapter, there is a numbered list entry labeled `65. blah-blah without any a or m` that misses its ending dot character `.`. Alas such an entry matches the chapter pattern which fools the documentation reconstruction into believing this is a real chapter...
- They are many typos in the original text e.g. look for occurrences of `yon` in place of `you` in chapter `2. Finding a Diamond on a Muddy Road`... Refer to `typo_and_fix` entries within [`Convert/StructuralInfo.py`](./Convert/StructuralInfo.py).

## Running the PDF converter with python

### Virtual environment set up

```bash {"name":"python-venv-install","terminalRows":"5"}
cd `git rev-parse --show-toplevel`/Convert
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py --help
```

### Running the converter

Within the above running context (directory and installed virtual environment)

```bash {"name":"python-venv-run","terminalRows":"5"}
cd `git rev-parse --show-toplevel`/Convert
source ./venv/bin/activate
python main.py
```

and the markdown default output should be placed in `output.md` file.

### Testing the conversion results

```bash {"name":"python-venv-test","terminalRows":"5"}
cd `git rev-parse --show-toplevel`/Convert
source ./venv/bin/activate
pip install -r requirements-dev.txt
python main.py --test
# and with a more verbose output:
pytest -vv test_main.py
```

### Developers: updating/overwriting the result_data contents

Once development has improved the resulting converted file, the following command will overwrite the reference resulting data

```bash {"name":"python-venv-overwrite-reference","terminalRows":"5"}
cd `git rev-parse --show-toplevel`/Convert
source ./venv/bin/activate
python main.py --output_directory ../result_data/
```

## Running the PDF converter with docker

```bash {"name":"docker-build-and-run"}
docker build -t jejune:convert_Zen_Flesh_Zen_Bones https://github.com/EricBoix/jejune_doc_Zen_Flesh_Zen_Bones.git#:DockerContext
docker run --rm jejune:convert_Zen_Flesh_Zen_Bones --help
```

Running the tests

```bash {"name":"docker-run-test"}
docker run --rm jejune:convert_Zen_Flesh_Zen_Bones --test
```

Extracting the result out of the container requires local filesystem mount

```bash {"name":"docker-run-output-extraction","terminalRows":"5"}
docker run --rm  -v `pwd`/junk:/output jejune:convert_Zen_Flesh_Zen_Bones --output_directory /output
```

and the result will be placed in a newly created `junk/` subdirectory.

## Running the PDF converter with jejune_cli

### Setting up jejune_cli context

Install and configure [`jejune_cli`](https://github.com/EricBoix/jejune_cli), then run `jejune doctor` to verify the configuration. This boils down to

```bash {"name":"jejune-cli-install","terminalRows":"20"}
cd `git rev-parse --show-toplevel`
uv tool install git+https://github.com/EricBoix/jejune_cli
jejune configuration doc-steward init     
# Proceed with the configuration of the files located in .jejune/ sub-directory.
# Assert the configuration is sound with
jejune doctor
```

Install the [`jejune_chunk_splitters`](https://github.com/EricBoix/jejune_chunk_splitters)
plugin (provides `jejune chunk-splitters split`):

```bash {"name":"jejune-cli-plugin-install"}
jejune plugin-packages install
```

### Running the converter (with jejune_cli)

Run the converter to extract a markdown out of the original PDF :

```bash {"name":"jejune-cli-convert"}
jejune convert build --no-cache
jejune convert run
```

where the output directory is default to `converted/` subdirectory.

To overwrite the reference converted files run

```bash {"name":"jejune-cli-run-overwrite","terminalRows":"5"}
cd `git rev-parse --show-toplevel`
jejune convert run --output-dir result_data
```

To run the converter tests inside the container:

```bash {"name":"jejune-cli-convert-test"}
jejune convert run --test
```

## Running the data workflow with jejune_cli

Define a convenience variable for the results directory:

```bash {"name":"jejune-cli-env-setup","terminalRows":"1"}
export RESULTS_DIR=`pwd`/result_data
```

Prepare the graph extraction by generating the various chunks with the splitters
(requires the [`jejune_chunk_splitters`](https://github.com/EricBoix/jejune_chunk_splitters)
plugin — see setup above):

```bash {"name":"jejune-cli-splitters-run"}
jejune chunk-splitters split --splitter headers
jejune chunk-splitters split --splitter paragraphs
jejune chunk-splitters split --splitter sentences
```

### Running Knowledge Graph extraction with a sentence granularity

```bash {"name":"jejune-cli-neo4j-cleanup"}
jejune neo4j delete $RESULTS_DIR    # Avoid collision with previous/other run
jejune neo4j stats --assert 0/0     # Just making sure deletion was effective
```

```bash {"name":"jejune-cli-graph-extract"}
jejune graph extract $RESULTS_DIR \
  --load_json_document \
    1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com_-_local_converter_-_Sentences_as_LangChain_document.json > llm_Sentences.log 2>&1 &
jejune neo4j stats --simple
jejune neo4j dump $RESULTS_DIR neo4j.ZenFleshZenBones.Sentences.dump
```

Extract knowledge graph in [Turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) format

```bash
jejune neo4j dump-turtle $RESULTS_DIR ZenFleshZenBones.Sentences.ttl
jejune neo4j stop
```

### Running Knowledge Graph extraction with a paragraph granularity

```bash {"name":"jejune-cli-neo4j-cleanup"}
jejune neo4j delete $RESULTS_DIR    # Avoid collision with previous/other run
jejune neo4j stats --assert 0/0     # Just making sure deletion was effective
```

```bash {"name":"jejune-cli-graph-extract-paragraphs"}
jejune graph extract $RESULTS_DIR   --load_json_document 1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com_-_local_converter_-_Paragraphs_as_LangChain_document.json > llm_Paragraphs.log 2>&1 &
jejune neo4j stats --simple
jejune neo4j dump $RESULTS_DIR neo4j.ZenFleshZenBones.Paragraphs.dump
```

```bash {"name":"jejune-cli-graph-convert-ttl-paragraphs"}
jejune neo4j dump-turtle $RESULTS_DIR ZenFleshZenBones.Paragraphs.ttl
jejune neo4j stop
```

### Running Knowledge Graph extraction with a markdown header granularity

```bash {"name":"jejune-cli-neo4j-cleanup"}
jejune neo4j delete $RESULTS_DIR    # Avoid collision with previous/other run
jejune neo4j stats --assert 0/0     # Just making sure deletion was effective
```

```bash {"name":"jejune-cli-graph-extract-headers"}
jejune graph extract $RESULTS_DIR \
  --load_json_document \
  1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com_-_local_converter_-_Headers_as_LangChain_document.json > llm_Headers.log 2>&1 &
jejune neo4j stats --simple
jejune neo4j dump $RESULTS_DIR neo4j.ZenFleshZenBones.Headers.dump
```

```bash {"name":"jejune-cli-graph-convert-ttl-headers"}
jejune neo4j dump-turtle $RESULTS_DIR ZenFleshZenBones.Headers.ttl
jejune neo4j stop
```
