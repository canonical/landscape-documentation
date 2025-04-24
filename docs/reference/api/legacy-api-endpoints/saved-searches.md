(reference-legacy-api-saved-searches)=
# Saved Searches


The methods available here are related to saved searches.

## CreateSavedSearch

Create a new saved search associated with the current account.

It requires three arguments:

`name`: The “slug” name for this saved search. It must consist of only lowercase ASCII letters, numbers and hyphens. This is the text which must be used when using the “search:name” syntax. If this parameter is not included a name will be generated automatically based on the title.
`title`: The display name for the saved search.
`search`: The search string to save.

For example, the following request creates a saved search associated with the account:

```text
?action=CreateSavedSearch&name=name1&title=Title%201&search=id:1
```

The method returns a JSON serialized version of the new saved search, like the following result:

```text
{
    "name": "first",
    "title": "First Computer",
    "search": "id:1"
}
```

## EditSavedSearch

Edit a saved search associated with the current account.

It takes three arguments:

`name`: The slug name for this saved search, this is the text which must be used when using the `search:name` syntax. A saved search with this name must already exist in the account.
`title`: The new display name for the saved search. If this parameter is not included then the title will not be modified.
`search`: The search string to save. If this parameter is not included then the search string will not be modified.

For example, the following request edits the title of a saved search associated with the account:

```text
?action=EditSavedSearch&name=name1&title=Title%201
```

The method returns a JSON serialized version of the new saved search, like the following result:

```text
{
    "name": "first",
    "title": "First Computer",
    "search": "id:1"
}
```

## GetSavedSearches

Retrieve saved searches associated with the current account.

It also supports two optional arguments:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

For example, the following request looks for saved searches associated with the account and limits the result to 20 saved searches:

```text
?action=GetSavedSearches&limit=20
```

The method returns a JSON serialized list of saved searches, like the following result:

```text
[
    {
        "name": "first",
        "title": "First Computer",
        "search": "id:1"
    }
]
```

## RemoveSavedSearch

Remove a saved search associated with the current account.

It requires one argument:

- `name`: The slug name for this saved search.

For example, the following request removes a saved search associated with the account:

```text
?action=RemoveSavedSearch&name=name1
```

