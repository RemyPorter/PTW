This will be a set of scripts that support a "plain text workflow". They'll provide simple, streamlined versions of common developer operations for the purpose of turning developer tools into author tools. If there's one thing programmers know, it's how to structure and manage reams of semantically significant text. In the end, this will kill the word processor.

There are two core packages at this time.

## Hashed
It accepts any string of hexadecimal characters and returns a string of words that uniquely maps to that hash.

```
>>> from hashed.words import dehash, enhash
>>> dehash("21046fd2f17ac0f30c88190393568045256866f2")
'cassareep irascibly upbrought scorched atheized bourtrees oloroso manful chobdar hornbook'
>>> enhash('disbowel obi magnetises famous oblivious divulgence thickened welders foiningly votresses')
'3bc491b57f3a4d1a91da3daae16dfa0052aff75f'
```

As a note, that module has broader uses, like making more readable representations of IPv6 addresses. It's currently weak on error handling, and will explode if you throw input at it that doesn't fit the wordlist.

### The Wordlist
The Wordlist is a space-padded file, with a word every 15 characters (or every 30 bytes). It was designed this way for fast access. There is also a JSON encoded index to support the reverse lookup.

## Bundle
The Bundle module is much more complicated. The purpose of this module is to take a set of resources defined in a "bundle file", munge them together into a Markdown file, and then process that Markdown file into a single-file HTML document. All stylesheets and images will be injected *inline*.

### The Bundle File
The Bundle grammar is defined thus:

```
PATH = CharsNotIn(",\n")("Path")
DESCRIPTION = Suppress(",") + restOfLine("Description")
ENTRY = Combine(PATH + Optional(DESCRIPTION))("entry")
SECTION = Combine(Suppress("#") + restOfLine("Section"))
STYLE = Combine(Suppress("$") + restOfLine("style"))
LINE = SECTION | ENTRY
BUNDLE = ZeroOrMore(STYLE) + ZeroOrMore(LINE)
```

A bundle starts with zero or more style entries. A style entry is a comma seperated list of stylesheet files on a line that starts with a dollar sign. After the style entries, the file can then contain any number of lines. Each line is either a section header ("#Some Section"), or a file entry. A file entry is simply the path to a file, optionally followed by a comma and a description/sub-header.

```
$core.css,extended.css,ebook-format.css
#Main
one.md
two.md,Heading 2
#Sub
three.md,Heading 3
```

Any section header ("#Main") will be injected into the output file as a markdown heading. Each file entry will be injected into the output file as raw data. If there's a description on the line ("Heading 2"), the description will precede the file's content as a sub-heading in Markdown. So, for example, this bundle would generate a markdown file like so:

```
#Main
[contents of one.md]
##Heading 2
[contents of two.md]
#Sub
##Heading 3
[contents of three.md]
```

### The Bundle object and Bundle Processor
```bundle.Bundle``` represents this bundle file. It has methods to load and write a file. ```bundle.BundleProcessor``` can take a ```bundle.Bundle``` object and generate the output file.

### Resources
The ```bundle.resources``` module is used for loading and injecting resources into an output HTML file. It has methods to load image resources, base64 encode them, and wrap them in a data:image URI. It also has methods to load a CSS file, and replace any url("") entries with image files. At this time, it is not compatible with images that are not referenced from the filesystem. (HTTP/FTP/etc. don't work)

### Markdownstyle
Using the ```bundle.Bundle``` object and the ```bundle.resources``` module, the ```bundle.markdownstyle``` module extends the core Python markdown library in several ways. First, it adds a markdown directive, [$img], which allows a user to embed image files in Markdown. When generating the HTML output, the [$img] tag will be replaced with an HTML img tag, and the file will be inserted via a datauri. Second, it takes the list of stylesheets from the Bundle object and injects them, inline, into the HTML output.

The result of calling the ```bundle.markdownstyle.MarkdownProcessor```'s ```markdown``` method will be an HTML file that contains all CSS and image resources referenced in the source files. This single file approach creates a simple to distribute output file.

## Notes
Now, the datauri schema bloats the file quite a bit. Reused images should be specified in the CSS, while inline images should be single-use figures or illustrations.