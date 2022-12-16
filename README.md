# sopel-spongemock
Sopel plugin to generate "Spongemock" text (based on *that* SpongeBob meme)

## Requirements

Only [Sopel](https://github.com/sopel-irc/sopel) itself.

## Installation

```sh
pip install sopel-spongemock
```

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
