# Azure Functions Setup Talk - Dec 13, 2019

Serverless functions are a deployment strategy (mostly used with micro services) that allows modules to be deployed and scaled independently from the rest of the application. In comparison with other PaaS or SaaS deployment strategies, FaaS (Functions as a Service) comply with the `event driven` architecture and gets instanciated when configured events are triggered making its cost management way more efficient.

## Goal

This project is intented to demonstrate the internals of a simple HTTP Triggered Azure Function and how it's deployed to Azure using Azure command line tools.

_**Side note:** There are Visual Studio Code extensions out there that provides IDE integration with Azure Functions. We intentionally decided to not use them in this presentation to be able to inspect what's going on behind the scenes._

## Getting Started

To optmize of setting up development environment, we decided to use [Vagrant][1] + [Ansible][2]. Just follow along to get your vm up and running.

Using a virtual environment is totally optional for the purposes of this demostration so feel free to go ahead and manually install the dependencies below on your current development environment if that works best for you. Simply jump straight to [setting up your local dev env](#setting-up-local-development-environment) below.

### Setting up the virtual development environment
- Download and install Virtualbox: [documentation][3]
- Download and install Vagrant: [documentation][4]
- Clone this repo to your local machine (You should be able to get this one done without further instructions, right??)
- Start a new console session and navigate to this project's [vagrant folder][5]
- Kick off Vagrant's automatic VM creation and provisioning by running `vagrant up`
- Once provisioning is complete, `vagrant ssh` into the machine and `cd /code`

`/code` is a mapping of the host's project folder into the VM, so you should have live access to any changes made in code from inside and outside of the virtual machine. Also, ports `7071` and `9091` are exposed from the VM so it's possible to access and debug your function running inside the VM from the host machine.

### Setting up local development enviroment

- Install Azure Functions Core Tools: [documentation][7]
- Instalar Azure CLI: [documentation][8]

_**Side note:** Although Azure Functions Core Tools provides all the functionality to create, test and deploy Azure Functions, Azure CLI is required to authenticate your current sessing in Azure. So before you try any cloud deployments from these command line tools, make sure you run `az login` first._

### Setting up Python

We chose Python for this project since most of our team is experienced C# and .Net developers.
It's intentional to offer new challenges to estimulate curiosity for new/different technologies.

[This is PyEnv's documentation][6] to get started installing custom versions of python on your box and how to create virtualenv (os independent area with custom python version and packages dedicated to your project).

Make sure you have `Python 3.7.5` and all dependencies from `requirements.txt` file.

### Setting up SendGrid

SendGrid is a great platform for sending emails and sms texts.
Many other configurations and features are available via their portal, such campaign management, reports and **TEMPLATES**!!

SendGrid offers free accounts plans that will be more than enough for the purposes of this demonstration.

Simply navigate to their [signup web page][9] and create your free account.
After loging, make sure you [create a new API Key][10] and then [create a new email template][11].

_**Side note:** Make sure you take note of the API Key generated. it's not going to be visible again after you close the confirmation page. A new API Key needs to be generated if you can't find yours._

_**Complimentary side note:** Make sure the API Key is stored in a safe place and never let it in your source control. Good development practices suggests that configuration must be stored out side of source code - [12Factor Principles][13]._

Feel free to reuse the pre-defined template sitting in this project's [templates folder](templates/).
All templates will be assigned a unique ID. This id will be used by our application so SendGrid knows how to prepare contents for the emails to be sent out.

Emails don't have to be static HTML, SendGrid supports template customization with loops conditions and much more by using [HandlebarsJS][12], a very popular javascript template rendering engine.

### Creating a new Function App in Azure

Log in to [Azure Portal][14] and choose `create a resouce`.
From the list presented, select for `Function App` and follow along with the wizard providing the Azure Subscription you'd like to have the function app associated with, region, resource groups and storage area for your app.

Remember that the Function App name has to be globally unique.

_**Side note:** Take note of Function App you just created. It will be required during the deployment phase._

This process will take a while... just so you know.

### Creating an Azure Function project

Sure this project provides you with a working Python HTTP Triggered Azure Function.
Still, you're highly encouraged to try it for yourself.

From the command line, try the following commands:
```
# create a python azure function project
func init --python PISetupTalkXmasMailer

# add a new http triggered function to your project
func new --template "Http Trigger" --name XmasHttpMailer

# run your newly created function locally
func host start
```

By default, python function templates create a boiler plate API endpoint that expects either GET or POST containing the paramenter "name".

If all went all in the commands above, you should be able to send requests to your local function at the URL from the web browser:
`http://localhost:7071/api/XmasHttpMailer?name=Setup%20Talk%20PI`.

The same result can be achieved from the command line.
```
# testing from the command-line
# using GET request
curl --get http://localhost:7071/api/XmasHttpMailer?name=Setup%20Talk%20PI
# using PUT request
curl --request POST http://localhost:7071/api/XmasHttpMailer --data '{"name":"Setup Talk PI"}'
```

### Implement SendGrid integration

In order to run the application locally, a few final configurations are required to have your app working properly in your local environment.

Activate your pyenv virtualenv (create one if you haven't done so yet).

Export local variables:
```
export SENDGRID_API_KEY='your-sendgrid-generated-api-key'
export SENDGRID_TEMPLATE_ID='newly-created-sendgrid-template-id'
```

Install python dependencies:
```
pip install -r requirements.txt
```

And finally, bring the application up once again:
```
func host start
```

This time, the app should expect also recipient's email as a new request parameter.
```
# testing from the command-line
# using GET request
curl --get http://localhost:7071/api/XmasHttpMailer?name=Setup%20Talk%20PI&email=mom@gmail.com
# using PUT request
curl --request POST http://localhost:7071/api/XmasHttpMailer --data '{"name":"Setup Talk PI", "email":"mom@gmail.com}'
```

### Publish to Azure

At this point, our Azure Function should be well tested and ready for Production.
To deploy it to the Azure, use the following command:

```
func azure functionapp publish SetupTalkXmasMailer
```

Keep in mind that `SetupTalkXmasMailer` should be replaced by the Azure Function App you created in Azure Portal.

## Found a bug? Suggestions?
Awesome, we all know noone is perfect and we'd love your feedback (and fixes Pull Requests).


[1]: https://vagrantup.com
[2]: https://ansible.com
[3]: https://www.virtualbox.org/wiki/Downloads
[4]: https://www.vagrantup.com/docs/installation/
[5]: vagrant/
[6]: https://github.com/pyenv/pyenv
[7]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools
[8]: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
[9]: https://signup.sendgrid.com/
[10]: https://sendgrid.com/docs/ui/account-and-settings/api-keys/#creating-an-api-key
[11]: https://sendgrid.com/docs/glossary/transactional-email-templates/
[12]: https://handlebarsjs.com/
[13]: https://12factor.net/config
[14]: https://portal.azure.com/
[15]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python