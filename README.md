stillson
========

Tool for generating config files using a template and environment variables.

[![Build Status](https://travis-ci.org/mortardata/stillson.png?branch=master)](https://travis-ci.org/mortardata/stillson)


# - why - #
Almost everything has a configuration file of some type these days. These config files range from very simple to fairly complex. If you happen to be using one of the many configuration management tools available they might provide a clean way to seperate content from values. Seperating the content from values lets you change the values easily based on context such as a common config serving multiple environments. Seperating values also lets you safely pull out secure values making it easy to check the configs into source control. However not everyone is running a configuration management tool and not every project calls for all the moving parts/processes of these configuration management tools. 

Stillson exists for the small plumbing projects where you just want to work with a configuration file in a shared manner while providing a clean way of pulling out secure credentials. Populating the values for your rendered template is left up to you and is made easy by stillson looking for environment variables that match what you setup in your templated config file. If envrionment variables are found for all of the template variables you defined then a config file is rendered. You can now use the rendered config file for your projects and tools.

# - how - #
## creating a config template ##
1. find the oroginal config file you wish to make into a template
    
    **example: starting config file widgets.conf**
    
    ```
    [service]
    username=joe
    password=god
    api_key=1234abcd
    
    [urls]
    webserver=dev.widget-company.com
    database=dbwebscale01.db.dev.widget-company.com
    ```
1. use variables to replace all secure values and things you want to change on rendering

    **example: starting config file widgets.conf.template**
    
    ```
    [service]
    username=${username}
    password=${password}
    api_key=1234abcd
    
    [urls]
    webserver=${environment}.widget-company.com
    database=${dbserver}.db.${environment}.${domain}
    ```  
 1. setup your source control to ignore the original config file and check in your template file 
 
    **git example: add .gitignore for widgets.conf and add widgets.conf.template**
    
    ```
        echo "widgets.conf" >> .gitignore
        git add .gitignore
        git add widgets.conf.template
        git commit -m "adding a template we can share for our widgets.conf file"
        git push

    ```
 
## rendering a config ##
Complete the following steps on your target machine to render a config file.
 
 1. on the target machines install stillson
  
     **example: install stillson system wide**
 
    ```sudo pip install stillson```
    
     **example: install stillson in virtualenv**
 
    ```
    mkdir -p /tmp/stillson-env
    virtualenv /tmp/stillson-env/ --no-site-packages
    cd /tmp/stillson-env
    source ./bin/activate
    pip install stillson
    ```
    
 1. check out your template file from source control
 1. create and set your environment variables for each of the variables in your template
  **example: widgets.conf.template variables**
    
    ```
    export username=joe
    export password=god
    export webserver=dev
    export dbserver=dbwebscale01
    export environment=dev
    export domain=widget-company.com
     ```
 1. run stillson to render your configuration file
 
    **example: render widgets.conf.template to stdout which can be redirected as needed**
 
    ``` stillson widgets.conf.template ```
    
    **example: render widgets.conf.template to /etc/widgetco/widgets.conf**
 
    ``` stillson widgets.conf.template -o /etc/widgetco/widgets.conf```
    

Note in the examples above we are manually exporting environment variables. You can use whatever preprocessing scripts, tools or human interactions for looking up the values and exporting them. 

## common errors ##

  * not setting an environment value for a variable in your templated config will give an error like:
  
  ```
  Traceback (most recent call last):
  File "/tmp/stillson-env/bin/stillson", line 8, in <module>
    load_entry_point('stillson==0.1.1', 'console_scripts', 'stillson')()
  File "/tmp/stillson-env/lib/python2.7/site-packages/stillson/stillson.py", line 59, in main
    render(template_path,output_file)
  File "/tmp/stillson-env/lib/python2.7/site-packages/stillson/stillson.py", line 34, in render
    raise StillsonMissingEnvVariable('The environment variable %s'%template_error)
stillson.stillson.StillsonMissingEnvVariable: The environment variable 'username' is not defined
  ``` 


![stillson](http://1.bp.blogspot.com/_AvVpqOzoWTg/S9pBbn9mRzI/AAAAAAAAAEo/o776hC6OBRc/s1600/pipewrench_00.jpg)


