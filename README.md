# certspotter processing tools

## Read certspotter configuration (the *watchlist*)

This component is a helper for the others. It interprets the watchlist and stores the information in a hierarchical domain tree.
The module also interprets comments in the watchlist (lines with leading `#`) and adds them to all subsequent lines as value.
For example:
```
# user@example.com
example.net
example.org
```
The value `user@example.com` is attributed to both subsequent domains.

## Read result file

This component is both a helper as well as a callable program.
It reads the output of certspotter (the *logs*) and interprets it.
The result is a Python dictionary with one entry per CTL-log entry. The `Filename` field is ignored.

The command line program can convert the certspotter logs into JSON format:
```bash
> python3 results.py certspotter-results.log certspotter-results.json
```
For input and output, stdin and stdout can be used as well, see `python3 results.py --help`.

## Sending

The last of the components combines all previous ones by processing the certspotter watchlist (default `~/.certspotter/watchlist`) and the certspotter-processing configuration (default `~/.config/certspotter_processing.ini`).

* Group the results by recipient:
```bash
> python3 sending.py group certspotter-results.log
```
Prints the results to stdout.

* Send the grouped results via RT:
```bash
> python3 sending.py send-rt certspotter-results.log
```

### Configuration

The configuration is in INI-format (Python's `configparser` module):
```ini
[rt]
uri=https://rtir.localhost.localt/rt/REST/1.0/
username=certspotter
password=<password>
queue=Investigations
```

## Run tests

```bash
> python3 test.py
```
