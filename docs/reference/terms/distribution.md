(reference-terms-distribution)=
# Distribution

In Landscape, the **distribution** refers to the Ubuntu operating system. There are different ways to specify the distribution depending on your use case.

There are some Landscape API methods and web portal features that require you to provide the distribution. For example, distributions are important if you want to mirror repositories via the web portal or API. For more information, see an [explanation of repository mirroring](https://ubuntu.com/landscape/docs/explanation-about-repository-mirroring).

## Example API methods that require a distribution

The following is a list of example Landscape API methods that require the distribution as a parameter:

- **Repositories**: These methods allow you to manage different repositories. For more information, see the [API methods on repositories](https://ubuntu.com/landscape/docs/api-repositories).

- **Reporting Methods**: These methods allow you to do reporting on selections of computers. They usually take the distribution as a query parameter. For more information, see the [API methods on reporting](https://ubuntu.com/landscape/docs/api-reporting).

- **Computers**: The methods under Computers help you retrieve computers and do basic operations such as tagging. With these methods, you can reference the distribution by using either the version number or the code name. For more information, see the [API methods on computers](https://ubuntu.com/landscape/docs/api-computers).
<br>
<br>
<br>

> *Thanks to the following contributor(s): [@ade555](https://github.com/ade555)*

