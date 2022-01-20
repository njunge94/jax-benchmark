# The `config` command

```shell
➜ pybm config -h
usage: pybm config get <option>
   or: pybm config set <option> <value>
   or: pybm config list
   or: pybm config describe <option>

Display and manipulate configuration values.

optional arguments:
  -h, --help  Show this message and exit.
  -v          Enable verbose mode. Makes pybm log information that might be useful for debugging.
```

The `pybm config` command is used to manipulate the configuration object underlying `pybm`. In that, it is rather
similar to the `git config` command.

## `pybm config get`

Values can be read with the `get` subcommand:

```shell
# default runner class is the timeit runner
➜ pybm config get runner.name
runner.name = pybm.runners.TimeitRunner
```

## `pybm config set`

To set a different value for an existing option, use the `set` subcommand:

```shell
# set a custom runner by specifying the class name
➜ pybm config set runner.name mypkg.MyRunner
```

## `pybm config list`

To list all available options and their current values, run `pybm config list`:

```shell
➜ pybm config list
Config values for group 'core':
datefmt : %d/%m/%Y, %H:%M:%S
envfile : .pybm/envs.toml
logfile : logs/logs.txt
logfmt : %(asctime)s — %(name)-12s — %(levelname)s — %(message)s
loglevel : 10
resultdir : results

Config values for group 'git':
basedir : ..

Config values for group 'builder':
name : pybm.builders.VenvBuilder
homedir : (empty string)
wheelcaches : (empty string)
venvoptions : (empty string)
pipinstalloptions : (empty string)
pipuninstalloptions : (empty string)

Config values for group 'runner':
name : pybm.runners.TimeitRunner
failfast : False
contextproviders : (empty string)

Config values for group 'reporter':
name : pybm.reporters.ConsoleReporter
timeunit : usec
significantdigits : 2

```

## `pybm config describe`

To get more information on a particular configuration value, run `pybm config describe` to get the corresponding value
type, its current value, and a small help text:

```shell
➜ pybm config describe runner.name
Describing configuration option 'runner.name'.
Value type:    str
Current value: 'pybm.runners.TimeitRunner'
Name of the runner class used in pybm to run benchmarks inside Python virtual environments. If you want to supply your own custom runner class, set this value to your custom subclass of pybm.runners.BaseRunner.
```