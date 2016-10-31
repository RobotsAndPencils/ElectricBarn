# ElectricBarn
Basic template for stubbing network requests with the MITMProxy libraries

Will dynamically replace network requests with the contents of json files that match the request or download the response from the real server and store it for future stubbing.

You need to have Xcode installed first.

## Install Homebrew and MITMProxy

ElectricBarn depends on MITMProxy, and the MITMProxy Python libraries. Because of the dependencies, we'll give ElectricBarn it's own Python install via [`pyenv`](https://github.com/yyuu/pyenv) and [`pyenv-virtualenv`](https://github.com/yyuu/pyenv-virtualenv)


1. Start by making sure you have [Homebrew](http://brew.sh/) installed
2. `$ brew update`
3. `$ brew install mitmproxy`

Now that we have mitmproxy we can put the (host-specific) mitmproxy certificate on your target device.

1. Make note of your Mac's local IP address (e.g. 192.168.1.12)
2. launch mitmproxy, telling it to listen on port 8888 `mitmproxy -p 8888`
3. Configure your iOS device's WiFi to use your Mac's IP as a *Manual* proxy, and set the port to 8888
4. Go to `mitm.it` in MobileSafari and install the "Apple" certificate on your iOS device.
5. Press `q` and then `y` to exit mitmproxy (Before quitting you can also load other pages and confirm that mitmproxy is indicating that it is intercepting the requests/responses)

## Install pyenv

3. `$ brew install pyenv`

> To upgrade `pyenv` in the future, use `upgrade` instead of `install`.
> After installation, you'll need to add `eval "$(pyenv init -)"` to your profile (e.g. `~/.profile`) (as stated in the caveats displayed by Homebrew — to display them again, use `brew info pyenv`). You only need to add that to your profile once.

This is what Homebrew outputs:

```
To use Homebrew's directories rather than ~/.pyenv add to your profile:
  export PYENV_ROOT=/usr/local/var/pyenv

To enable shims and autocompletion add to your profile:
  if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
```

Before we do this ^ let's install `pyenv-virtualenv`

## Install pyenv-virtualenv

Original instructions to [Install pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installing-with-homebrew-for-os-x-users)

1. `brew install pyenv-virtualenv` or `brew install --HEAD pyenv-virtualenv`
2. Add the following to your `~/.profile`

`if which pyenv > /dev/null; then eval "$(pyenv init -)"; eval "$(pyenv virtualenv-init -)"; fi`

Then start using your updated profile:

`source ~/.profile`

## Create mitm-specific environment
`pyenv` and `pyenv-virtualenv` make it easy to have a project-specific python install. This helps keep your machine clean from conflicting dependencies, etc.

First give `pyenv` a fresh install of Python3.5 to use

`$ pyenv install 3.5.1`

_Note: may need to use `PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs2" pyenv install 2.7.10`_

Then let's create a virtualenv from this version of python

`$ pyenv virtualenv 3.5.1 mitmproxy-env-3.5.1`

This created a `mitmproxy-env-3.5.1` with the 3.5.1 version of python that we'll use with the `mitmproxy` libraries.

We want to activate our environment, but first let's get the name of the virtualenv we want to activate

`$ pyenv virtualenvs`

which lets us see that we can use

`$ pyenv activate mitmproxy-env-3.5.1`

Now we should be able to install mitmproxy (v0.18.2 is currently the latest version)

`$ pip install mitmproxy`

you should now be able to run `./electricbarn.py` from the `mitm` directory. 

Any file in the subfolders will be stubbed for a matching request.

When you are done you should be able to kill `electricbarn.py` with at ctrl+c, and then `pyenv deactivate` to disable this virtual environment.

Take a look at https://github.com/mitmproxy/mitmproxy/tree/master/examples for some other examples (such as adding header values with a script). It would be pretty easy to copy `electricbarn.py` and make a custom proxy that does what you need to matching requests.

Note: You probably need to make sure that your iOS project has *only* the following ATS keys in the plist of the app (or else ATS will prevent MITMProxy or its python libraries from intercepting requests)
```
	<key>NSAppTransportSecurity</key>
	<dict>
		<key>NSAllowsArbitraryLoads</key>
		<true/>
        <key>NSExceptionAllowsInsecureHTTPLoads</key>
        <true/>
        <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
        <true/>
	</dict>
```
