passtools-python
==============

Official Python SDK for the PassTools API The SDK make is easy to manage Apple Passbook passes through the PassTools API.

## Resources 

* Please refer to the [API Doc](https://github.com/tello/passtools-api) for the raw apis.
* [Indexed documentation for the python SDK](http://tello.github.com/passtools-python/) is available.
* There are also commented example scripts available in the "Example_Scripts" directory of the installation. These scripts include examples of all available calls as well as a couple of real-world-like scenarios.

## Installation

### Via pypi.org

`$ pip install passtools`

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- or - 

### Local tar

* Download the archive
* Unzip and untar
`$ gunzip < PassTools-1.0.0.tar.gz | tar xf -`
* cd into the new directory
`$ cd PassTools-1.0.0`
* Run setup
`$ python setup.py install`

## Usage

####Import and configuration

In all of your scripts, start by configuring PassTools, passing it your API key. Your API key is private, and allows you secure API access. Your API key is available from the Account Settings/API Key pages of the PassTools web application. Configure PassTools like this:

`from passtools import PassTools`

`PassTools.configure(api_key = my_api_key)`

If your script will involve templates, you'll want to import Template, if Passes, import Pass:

`from passtools.pt_template import Template`

`from passtools.pt_pass import Pass`

#### Working with PassTools Templates:

There are 3 class methods available:

####Template.list()

Return a list of template _headers_ associated with the specified api_key. list() can accept optional filter arguments--see the docstring API help.

####Template.get(template_id)

Return the complete template object specified by the supplied ID.

####Template.delete(template_id)

Delete the template specified by the supplied ID.

#### Working with PassTools Passes:

There are 9 class methods available:

####Pass.list()

Return a list of template _headers_ associated with the specified api_key. list() can accept optional filter arguments--see the complete API help.

####Pass.get(pass_id)

Return the complete pass object specified by the supplied ID.

####Pass.delete(pass_id)

Delete the pass specified by the supplied ID.

####Pass.create(template_id, template_fields_model_dict)

Create a new pass based upon the supplied template (specified by ID and fields_model).

####Pass.update(pass_id, update_fields)

Update an existing pass, specified by ID, using the supplied data.
The update() method does _not_ update passes already installed on devices; see push_update() for that.

####Pass.push_update(pass_id)

Update any installed passes, specified by ID. Typically, the sequence might be:

* Create a template using PassTools TemplateBuilder
* From that template, create a pass (either via the API or the UI)
* Distribute the pass to users who install it on their devices
* Use update() to update the pass (this changes only the in-PassTools copy)
* Use push_update to update the installed passes in realtime

####Pass.download(pass_id, destination_path)

Download a pass specified by the supplied ID. This pass can be distributed to users via email, for instance.

####Pass.add_locations(pass_id, location_list)

Add 'Relevant Locations' to an existing pass, specified by ID, using the supplied data.

That data must be in the form of a list of location dicts, for example:

`data = [{"latitude"=>37.4471107, "longitude"=>-122.16206219999998, "streetAddress1"=>"408 Florence St", "streetAddress2"=>"", "city"=>"Palo Alto", "region"=>"CA", "regionCode"=>"94301", "country"=>"US", "relevantText"=>"Palo Alto Office!"}]`

####Pass.delete_location(pass_id, location_id)

Delete a 'Relevant Location' from an existing pass. Both pass and location are specified by integer IDs.


## Examples

Scenario: Say you wanted to create a personalized coupon for one of your customers, "Marie Lie". 
The pass personalization and generation will be handled by your script via the PassTools API, but the initial layout and design of the pass "Template" will be done using the PassTools web UI. So...

* Create a Coupon template through the PassTools UI. In our example, you decide to create secondary fields to capture the first and last name of your customer, and you give those fields custom keys for your own convenience: _first_name_, _last_name_.

* When you've completed and saved the template, you check the template list page to get the ID for your new template. For this example, say the ID is 5.

* Now let's write the script: 

Start by configuring PassTools, passing it your API key. 

```python
from passtools import PassTools
from passtools.pt_pass import Pass
from passtools.pt_template import Template
PassTools.configure(api_key = my_api_key)
```

Next, retrieve your newly created template:

```python
template_get_response = Template.get(5)
template_fields_model = template_get_response['fieldsModel']
```

The template object includes a 'fields_model'--a dict comprised of the keys and values you specified when you created the template. As mentioned above, when you defined this template, you assigned custom key names to two secondary fields...so now use those key names to refer to the fields you want to set with your customer information:

```python
template_fields_model["first_name"]["value"] = "Marie"
template_fields_model["last_name"]["value"] = "Lie"
```

Next, create Marie's pass 

```python
create_response = Pass.create(5, template_fields_model)
```

And finally, you can download the pass...
(the file _must_ have a ".pkpass' extension to be properly handled when delivered to your customer's iOS device.)

```python
Pass.download(create_response['id'], "/tmp/Marie_Lie.pkpass")
```     
The pass is downloaded to your local filesystem. 

You can now deliver the pass to Marie by email, sms, or through a hosted URL.

#####You will find several other simple example scripts in the SDK.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request



