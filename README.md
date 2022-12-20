# sopel-spongemock
Sopel plugin to generate "Spongemock" text (based on *that* SpongeBob meme)

## Requirements

**Basic usage:** Only [Sopel](https://github.com/sopel-irc/sopel) itself.

**With configurable output:** Additionally requires the `spongemock` PyPI package.

**More robust Unicode detection:** Additionally requires the `unicodedata2` PyPI package.

## Installation

**Basic**
```sh
pip install sopel-spongemock
```

**Configurable**
```sh
pip install sopel-spongemock[lib]
```

**Robust**
```sh
pip install sopel-spongemock[ud2]
```

***Note:** It is possible to install both `lib` and `ud2` extras at once, but
doing so serves no purpose; the `spongemock` package does not make use of
`unicodedata` or `unicodedata2`.*

## Configuration

If installed with the `lib` extra, use the following template in Sopel's
configuration file to set options for `spongemock`'s output:

```ini
[spongemock]
diversity_bias = 0.6
always_start_lower = False
```

The `diversity_bias` option controls the chance of switching cases for each
letter in the output. `0.0` represents a perfectly random, 50/50 chance.
Higher values increase the likelihood of switching as more consecutive
letters are output with the same case. At `1.0`, it's guaranteed that the
case will switch for every letter.

**Values outside the range of [0.0, 1.0] will cause errors.**

Feel free to experiment with intermediate values to find what "looks right"
for your own interpretation of the mocking-text meme.

The `always_start_lower` option will output `text.swapcase()` if the first
letter of the output is capitalized. (While the built-in mocker always starts
with lowercase, the external library sets case of the first letter randomly.)

***Note:** Options in this configuration section have no effect if the plugin
is installed without the `lib` extra.*

## Usage

```
.spongemock <nick>|<text>

or

.smock <nick>|<text>
```

If a single word is passed, the command will first check if that nick has said
anything in the channel recently, and will mock their last message if so.

Any input that does not match a known user's nick will be mocked directly.

### Examples

```
<dgw> .smock Free speech!
<Sopel> fREe SpEEcH
```

```
<dgw> I'm something of a Pythonista myself
<ziro> .smock dgw
<Sopel> i'M soMeThiNg oF a pYtHOnIsTA mySElf
```
