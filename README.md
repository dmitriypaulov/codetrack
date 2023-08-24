# Codetrack
Open-Source Telegram bot where you can save and share code snippets

## Project Setup

### Requirements
```
pip3 install -r requirements.txt
```

### Translations Updation
#### Initialize or update translations

Put any language code instead of **\<LOCALE>** parameter.
For example uk for Ukrainian, de for German etc

Use commands below to initialize locale translations, then update translations manually in **locales/\<locale>/LC_MESSAGES/codetrack.po**

```
pybabel extract --input-dirs=. -o locales/codetrack.po
pybabel init -i locales/codetrack.po -d locales -D codetrack -l <LOCALE>
```

#### Compile translations
After initialization or updation you need to compile changes.

```
pybabel compile -d locales -D codetrack
```

