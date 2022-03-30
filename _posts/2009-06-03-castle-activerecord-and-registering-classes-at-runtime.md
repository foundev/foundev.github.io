---
title: Castle ActiveRecord and registering classes at runtime
date: 2009-06-03T06:02:00+00:00
author: Ryan Svihla
layout: post
tags: [csharp]
---
*EDIT: this is an old post copied over from my [old blog on Los Techies](https://lostechies.com/ryansvihla/2009/06/03/castle-activerecord-and-registering-classes-at-runtime/), I have kept it here for archival reasons.*

I use the following trick for adding ActiveRecord classes after the fact for our in-house plug-in architecture. Thanks to whichever blogger/mailing list I picked this up from so long ago.

## Scenario 1: Class(es) to load inherit from same base class as current running ActiveRecord classes

```csharp
var holder = ActiveRecordMediator.GetSessionFactoryHolder();
//register your subclasses here
ActiveRecordStarter.RegisterTypes(typeof(Employee), typeof(Customer));

holder.RegisterSessionFactory(
    holder.GetConfiguration(typeof(ActiveRecordBase)).BuildSessionFactory(), typeof(ActiveRecordBase)
);
//reloads session factory without this types will not be registered. 
//I believe this is actually a "feature" in Castle trunk. may be fixed now.
```

This is all you need to register extra classes that are accessing the same database as the application is using.

## Scenario 2:Not only must the new types be registered but a new base class with its new configuration as well

```csharp
InPlaceConfigurationSource source = new InPlaceConfigurationSource();
// config. change this to suite your needs
Dictionary<string, string> confdict = new Dictionary<string, string>
    {
        {"connection.driver_class", "NHibernate.Driver.SqlClientDriver"},
        {"dialect"    ,"NHibernate.Dialect.MsSql2000Dialect"},
        {"connection.provider","NHibernate.Connection.DriverConnectionProvider"},
        {"connection.connection_string","Data Source=localhost;Initial Catalog=intranet_devel;Integrated Security=SSPI"},
        {"proxyfactory.factory_class","NHibernate.ByteCode.Castle.ProxyFactoryFactory, NHibernate.ByteCode.Castle"}
    };
source.Add(typeof(BaseCRMobj), confdict);
var holder = ActiveRecordMediator.GetSessionFactoryHolder();
var config = new Configuration(); 
foreach (var conf in source.GetConfiguration(typeof(BaseCRMobj)).Children)
{
    //turns ActiveRecord config Configuration could be skipped if you load Configuration object instead
    config.Properties[conf.Name] = conf.Value;
}
// loads the base type and its configuration into ActiveRecord
holder.Register(typeof(BaseCRMobj), config);
//reloads sessionfactory again note not using ActiveRecordBase now
holder.RegisterSessionFactory(holder.GetConfiguration(typeof(BaseCRMobj)).BuildSessionFactory(), typeof(BaseCRMobj)); 
```

After you have configured the base type for your ActiveRecord classes plus its connection string then call the register types method again:

```csharp
var holder = ActiveRecordMediator.GetSessionFactoryHolder();
// register individual subclasses
ActiveRecordStarter.RegisterTypes(typeof(Employee), typeof(Customer));
//reloads instance of SessionFactory
holder.RegisterSessionFactory(holder.GetConfiguration(typeof(BaseCRMobj)).BuildSessionFactory(), typeof(BaseCRMobj));
```

Overall this works quite well even if its noisy . I am able to dynamically load connections to 5 different databases and register a hundred or so classes total, all after the application has started. The real code has some DRY cleanup going on but this is more or less what I really use.

