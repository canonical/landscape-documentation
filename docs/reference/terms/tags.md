---
myst:
  html_meta:
    description: "Reference for Landscape tags used to organize and group client instances with user-defined labels and metadata."
---

(reference-terms-tags)=
# Tags

**Tags** are user-defined labels or metadata that can be used to organize your client instances in Landscape. Landscape lets you group multiple instances by applying tags to them. Tag names may use any combination of letters, numbers, and dashes, and each instance can be associated with multiple tags. You can group instances using any set of characteristics; Ubuntu series and location might be two logical tagging schemes. For example, if you are managing an instance based in London running on Ubuntu 24.04 LTS Noble Numbat, you could associate both "noble" and "eu-west-2" tags to it. 

## Working with tags

### In the new web portal
You can assign tags from the **Instances** tab by selecting a list of instances and then selecting **Assign** > **Tags**. You can also add or remove tags from a single instance by navigating to its page and selecting **Edit**. 

### In the classic web portal
There is no menu choice for tags; rather, you can navigate to **Computers** > **Info** to apply or remove one or more tags to all the instances you have selected. If you want to specify more than one tag at a time for your selected instances, separate the tags by spaces.

### Via the API
See the Legacy API reference for {ref}`adding <header-add-tags-to-computers>` and {ref}`removing <header-remove-tags-from-computers>` tags from client instances.
