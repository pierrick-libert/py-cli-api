# Markdown

The purpose of this file is to briefly explain how I decided to work on the project, what's missing and the potential improvements I could implement.

## Technical Choice

I decided to go with Python since its scripting style and the possibility to type the code is a good match for this kind of project.

I just added libraries to control the code quality and to facilitate the communication with the DB.

My implementation is very strict when it comes to typings with Python. Though it's definitely not mandatory with the language, I think that's a good practice to keep in order to ease the readability of the code.

### Implementation

Few comments about my implementation.

I decided to use `argparse` to control the command line arguments and parsing since it makes the work much easier with the built-in methods inside it. Recoding a system by myself was a waste of time in my own opinion.

I dynamically instantiate the module with `getattr` since it avoid to have a long list of `if/elif/else` but I decided to avoid the dynamic call on method to avoid to have `def method(self, *args, **kwargs)` which I found not really readable and maintainable in this case.
I gathered `create` and `update` under an `upsert` method since I can use a specific method in the ORM for this.

I created `TRIGGER` and `FUNCTION` to handle cases of up/down update on `is_active` field for the different models. I found this solution as the quickest to implement and to execute. However, I'm aware that it terms of maintainability it may be complicated and a good documentation is necessary.

I also decided to add `display_name` and `slug` for all models to make it consistent between tables.

## Functionalities

Almost of features have been implemented according to the subject.

However one important, and mentioned in the document, feature is missing.
The filter on children for search with threshold.
In my implementation, you may see a `prefix` variable when I'm building the `where`, I used this system to add a `JOIN` in the base request and an alias on the joined table. Then, in the data, I would have added a `child: bool` value to mention if the filter must be applied on the parent or child's fields.

## Improvements

Numerous improvements could be set in this project.

 * Probably one of the most important: creating unit test to check the stability in the program
 * A kind of serializer to control the JSON data sent on most call, to make the remaining code lighter in verification and throw an error from the beginning
 * Setting up a migration tool such as `Alembic` to have a better control on the DB
 * Translations table for all models
