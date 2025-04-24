(reference-rest-api-packages)=
# Packages

## GET `/packages`

Get packages associated with a computer ID.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `query`: A query string used to select computers to query packages on. 
- `search`: A string to restrict the search to (optional). All fields are searched, not just those returned. (e.g., description)
- `names`: Restrict the search to these package names. Multiple names can be specified by numbering the names with `names.1`, `names.2`, etc.
- `installed`: If true only packages in the installed state will be returned, if false only packages not installed will be returned. If not given both installed and not installed packages will be returned.
- `available`: If true only packages in the available state will be returned, if false only packages not available will be returned. If not given both available and not available packages will be returned.
- `upgrade`: If true, only installable packages that are upgrades for an installed one are returned. If false, only installable packages that are not upgrades are returned. If not given, packages will be returned regardless of whether they are upgrades or not.
- `held`: If true, only installed packages that are held on computers are returned. If false, only packages that are not held on computers are returned. If not given, packages will be returned regardless of the held state.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

