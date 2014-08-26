This will be a set of scripts that support a "plain text workflow". They'll provide simple, streamlined versions of common developer operations for the purpose of turning developer tools into author tools. If there's one thing programmers know, it's how to structure and manage reams of semantically significant text. In the end, this will kill the word processor.

The hashed package is the only thing complete at this time. It accepts any string of hexadecimal characters and returns a string of words that uniquely maps to that hash.

```
>>> import hashed.words
>>> hashed.words.dehash("21046fd2f17ac0f30c88190393568045256866f2")
FriendlyHash(hash='21046fd2f17ac0f30c88190393568045256866f2', friendly='cassareep irascibly upbrought scorched atheized bourtrees oloroso manful chobdar hornbook')
```

As a note, that module has broader uses, like making more readable representations of IPv6 addresses.