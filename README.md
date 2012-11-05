passtools-python
==============

Official Python SDK for the PassTools API The SDK make is easy to manage Apple Passbook passes through the PassTools API.

## Resources 

* Please refer to the [API Doc](https://github.com/tello/passtools-api) for the raw apis.
* This repo includes docstring documentation; please direct your browser to the index.html in the html dir to read that.
* There are also commented example scripts available in the "Example_Scripts" directory of the installation. These scripts include examples of all available calls as well as a couple of real-world-like scenarios.

## Installation

* Download the archive
* Unzip and untar
`gunzip < PassTools-1.0.0.tar.gz | tar xf -`
* cd into the new directory
`cd PassTools-1.0.0`
* Run setup
`python setup.py install`

## Example Usage

Scenario: Say you wanted to create a personalized coupon for one of your customers, "Marie Lie". 
The pass personalization and generation will be handled by your script via the PassTools API, but the initial layout and design of the pass "Template" will be done using the PassTools web UI. So...

* Create a Coupon template through the PassTools UI. In our example, you decide to create secondary fields to capture the first and last name of your customer, and you give those fields custom keys for your own convenience: _first_name_, _last_name_.

* When you've completed and saved the template, you check the template list page to get the ID for your new template. For this example, say the ID is 5.

* Now let's write the script: 

In all of your scripts, start by instantiating a pt_service.Service object, passing it your API key. Your API key is private, and allows you secure API access to your Templates, Passes, and related information. To obtain your API key, contact PassTools at help@passtools.com. 

```python
from passtools import pt_service, pt_pass

api_key = "your-key-goes-in-here"

the_service = pt_service.Service(api_key)
```

Next, call _Service.get_template()_ to retrieve your newly created template

```python
the_template = the_service.get_template(5);
```

The template object includes a 'fields_model'--a dict comprised of the keys and values you specified when you created the template. As mentioned above, when you defined this template, you assigned custom key names to two secondary fields...so now use those key names to refer to the fields you want to set with your customer information:

```python
the_template.fields_model["first_name"]["value"] = "Marie"
the_template.fields_model["last_name"]["value"] = "Lie"
```

Next, create Marie's pass 

```python
new_pass = pt_pass.Pass(5, the_template.fields_model)
```

And finally, you can the pass...
(the file _must_ have a ".pkpass' extension to be properly handled when delivered to your customer's iOS device.)

```python
new_pass.download("/tmp/Marie_Lie.pkpass")
```     
The pass is downloaded to your local filesystem. 

You can now deliver the pass to Marie by email, sms, or through a hosted URL.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request



