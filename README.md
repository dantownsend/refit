# Refit

[![Documentation Status](https://readthedocs.org/projects/refit/badge/?version=latest)](https://refit.readthedocs.io/en/latest/?badge=latest)

Simple remote server configuration and deployment, using asyncio. [Read the Docs](https://refit.readthedocs.io/en/latest/).

## Why Refit?

As a die hard Ansible user for many years, I started looking for something slightly different.

Because of Docker, most of my deployments have become simpler. It usually involves uploading some files (e.g. `docker-compose.yaml`), and running some shell commands (e.g. `docker-compose up`). As a result, I don't need most of the modules that Ansible provides.

One thing I originally found great about Ansible was being able to configure it purely in YAML. This is nice when you're getting started. As your projects get larger though, you yearn for the control that code gives you. For example, rather than having to learn the particular syntax for performing 'for loops' in YAML, just do it naturally in Python.

Ansible is still great - but if you want to work in Python rather than YAML, give Refit a go.

### Isn't it all about serverless nowadays?

Configuring servers is still a daily reality for many people, and will continue to be so for the foreseeable future. Need websockets? Can't stand the slow start up times of serverless? Want to avoid vendor lock in? Using VMs still makes a lot of sense.

### Why asyncio?

Asyncio is a new approach to concurrency which was added in Python 3. It uses an event loop, rather than threads or processes. A typical use case is building a proxy, or a higher throughput web application.

It turns out that asyncio also works great for remote server configuration too. The reason is, your typical server config work flow looks a bit like this:

```
   MACHINE A          MACHINE B
   ---------          ---------
(TASK A1, TASK A2)     TASK B1
       |                  |
    TASK A3               |
                       TASK B2
```

Using async, we can fire off tasks A1, A2, and B1 simultaneously. Once complete, we then fire off task A3, and finally task B2. Refit will orchestrate the tasks so the servers are provisioned as quickly as possible.

It also means you can use all the exciting new asyncio libraries within your code.

## Props

Built on top of the great work done in [asyncssh](https://github.com/ronf/asyncssh).
