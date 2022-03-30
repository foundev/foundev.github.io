---
wordpress_id: 53
date: 2011-09-25T12:04:54+00:00
author: Ryan Svihla
layout: post
wordpress_guid: http://lostechies.com/ryansvihla/?p=53
dsq_thread_id:
  - "425495610"
tags:
  - CI
  - Rails
---
<h1>Rail 3.1 CI setup with Jenkins, Test Unit &#038; SimpleCov on OS X Lion.</h1>
I recently had to setup a build server for some rails work I'm doing. Still wanting to support my other projects I setup Jenkins. I ran into several issues.

## Running Jenkins as a hidden user

First I noticed that jenkins was running as the "daemon" user, this obviously wasn't going to work for github and rvm needs. So I did some googling and had some guides to get Jenkins running as a specific user. I did the following (sourced from http://colonelpanic.net/2011/06/jenkins-on-mac-os-x-git-w-ssh-public-key/ ).

```bash
sudo dscl . create /Users/jenkins
sudo dscl . create /Users/jenkins PrimaryGroupID 1
sudo dscl . create /Users/jenkins UniqueID 300
sudo dscl . create /Users/jenkins UserShell /bin/bash
sudo dscl . passwd /Users/jenkins $PASSWORD
sudo dscl . create /Users/jenkins home /Users/Shared/Jenkins/Home/
```

Note: That's really $PASSWORD up above. This gives you a prompt to enter that password. Next you'll need to stop the Jenkins service and edit the plist and start the service back up.

```bash
sudo launchctl unload -w /Library/LaunchDaemons/org.jenkins-ci.plist
sudo vim /Library/LaunchDaemons/org.jenkins-ci.plist
sudo launchctl load -w /Library/LaunchDaemons/org.jenkins-ci.plist
```

You're plist file should end up like this.

<img title="file_to_edit.png" src="/assets/file_to_edit.png" border="0" alt="File to edit" width="600" height="355" />

## RVM issues

Now my next issue was despite what I&#8217;d read elsewhere I was unable to get Jenkins to use the default ruby provided by RVM. So I just pasted the commands that I would run anyway in the &#8220;Execute Shell&#8221; build step.

<img title="rvm_workaround.png" src="/assets/rvm_workaround.png" border="0" alt="Rvm workaround" width="600" height="161" />

## Getting Jenkins to see tests

I&#8217;ve been using Test:Unit/Minitest lately just to keep more consistent with my day to day work. However I haven&#8217;t found a way to get my tests to show when using the &#8220;Execute Shell&#8221; task. I found a little gem called ci_reporter that exports to the standard junit format, unfortunately it doesn&#8217;t work with minitest yet. That&#8217;s ok I haven&#8217;t done anything that Test:Unit doesn&#8217;t support so far so I added the the following to my Gemfile (note the part about unit-test 2.0):

```ruby
group :development, :test do
  gem 'ci_reporter', '1.6.3'
  gem 'test-unit', '~&gt; 2.0.0'
  # Pretty printed test output
  gem 'turn', :require =&gt; false
end
```

Running &#8220;rake ci:setup:testunit test&#8221; should give you a bunch of xml files in tests/reports. Now we need to tell Jenkins where to find those reports so add a post build action to pick them up as junit reports.

<img title="post_build_actions.png" src="/assets/post_build_actions.png" border="0" alt="Post build actions" width="600" height="82" />

## Rcov reports

This was pretty easy.

  1. Install Jenkins plugin for RCov (it's in the plugin list in the admin section).
  2. add simplecov and semiplecov-rcov to your Gemfile.
  3. add the following 4 lines to the TOP of your tests/test_helper.rb file:

```ruby
require 'simplecov'
require 'simplecov-rcov'
SimpleCov.formatter = SimpleCov::Formatter::RcovFormatter
SimpleCov.start 'rails'
```



## In closing

This took a fair amount of time, but the end result was quite satisfying. I now have CI with tests, tests coverage, RVM to target different versions of Ruby and bundler to make sure my Gem environment is sane.