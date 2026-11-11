# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Running things](#running-things)
- [Testing](#testing)
- [Converter developers](#converter-developers)
- [Converter limitations and things to fix](#converter-limitations-and-things-to-fix)

## Running things

Refer to [repository README.md](../README.md#converter-with-python)

## Testing

Within the above running context (directory and installed virtual environment)

```bash
pytest test_main.py
```

## Converter developers

When `pdf-to-markdown` is upgraded you must run

```bash
uv lock --upgrade-package pdf-to-markdown
```

proceed with fixing/upgrading things and commit `uv.lock` and the resulting code modifications.

## Converter limitations and things to fix

- Page 15 finishes with the following sentence:
  
  ```text
  ‘I am Gudo of Kyoto and I am going on to Edo,’ replied the Zen master.
  ```

  that gets rejected by `Sentence::is_complete()` (that is it is considered as an un-complete sentence because its first character is not a capital letter). How to improve on this ?
