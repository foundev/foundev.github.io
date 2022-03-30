---
date: 2009-05-22T00:21:00+00:00
author: Ryan Svihla
layout: post
tags: [csharp, testing]
---
<h1>Context and Spec style testing and my approach to BDD</h1>
*EDIT: this is an old post copied over from my [old blog on Los Techies](https://lostechies.com/ryansvihla/2009/05/22/context-spec-style-testing-and-my-approach-to-bdd/), I have kept it here for archival reasons.*


I borrow heavily my approach to testing from a combination of Ayende's [Rhino Tools](http://rhino-tools.svn.sourceforge.net/viewvc/rhino-tools/trunk/) tests, and my reading of the [Rspec](http://www.pragprog.com/titles/achbd/the-rspec-book) beta book. But I think I've stumbled onto something I'm happy with and I can generate reports out of. Let's go over some basic rules first:

  1. Move as much common setup logic to a base class as possible. 
  2. Use your class name as the context 
  3. methods are rules beginning with should; 
  4. create a new subclass of the base context every time you have a new scenario

Code ends up looking like so: 

```csharp
public class BaseAddVacationContext
    {
        protected AddVacationRequest _submission;
        protected IEmailSender _sender;
        protected IUserInformation _information;
        protected ICrudRepo<LeaveRequest> _leaverepo;
        protected LeaveRequest _request;

        [SetUp]
        public virtual void SetUp()
        {
            _sender = MockRepository.GenerateMock<IEmailSender>();
            _information = MockRepository.GenerateMock<IUserInformation>();
            _leaverepo = MockRepository.GenerateMock<ICrudRepo<LeaveRequest>>();
            _submission = new AddVacationRequest(_sender, _information, _leaverepo);
            _request = new LeaveRequest() { UserName = "userman" };
           
            
        }
    }
    [TestFixture]
    public class SpecAddVacationRequestWhenEmployeeSubmitsRequest : BaseAddVacationContext
    {
      
        [SetUp]
        public override void SetUp()
        {
            base.SetUp();
            _information.Stub(x => x.GetManagersEmailAddresses("userman")).Return(new[] { "manager1@jonbank.com", "manager2@jonbank.com" });
            _information.Stub(x => x.GetReviewersEmailAddress("userman")).Return(new[] { "james@jonbank.com", "jones@jonbank.com" });
            _information.Stub(x => x.GetUserEmail("userman")).Return("userman@jonbank.com");
            _submission.Execute(_request);
            
        }

        [Test]
        public void should_email_all_managers()
        {
            _sender.AssertWasCalled(x => x.Send(Arg<Message>.Matches(y => y.To == "manager1@jonbank.com")));
            _sender.AssertWasCalled(x => x.Send(Arg<Message>.Matches(y => y.To == "manager2@jonbank.com")));
        }

        [Test]
        public void should_send_email_to_user()
        {
            _sender.AssertWasCalled(x => x.Send(Arg<Message>.Matches(y => y.To == "userman@jonbank.com")));
        }

        [Test]
        public void should_store_leave_request_in_database()
        {
            _leaverepo.AssertWasCalled(x=>x.Create(Arg<LeaveRequest>.Matches(u=>u == _request)));
        }

        [Test]
        public void should_email_all_reviewers()
        {
            _sender.AssertWasCalled(x => x.Send(Arg<Message>.Matches(y => y.To == "jones@jonbank.com")));
            _sender.AssertWasCalled(x => x.Send(Arg<Message>.Matches(y => y.To == "james@jonbank.com")));
        }
    }
    [TestFixture]
    public class SpecAddVacationRequestWhenRequesWasAlreadyMadeForThoseDays : BaseAddVacationContext
    {
      
        [SetUp]
        public override void SetUp()
        {
            base.SetUp();
            
            _leaverepo.Stub(x=>x.Create(null)).Throw(new EmployeeAlreadyRequestedTheseDaysOff()).IgnoreArguments();
         }
         [Test]
         public void should_not_send_email_to_anyone()
	 {
            
           _sender.AssertWasNotCalled(x => x.Send(Arg<Message>.Is.Anything));
         }
    }
```

So here we have: 

  * A setup that you need to override and call to setup context specific behavior 
  * small small tests and asserts. 
  * limited setup on mocks, you can use handrolled mocks or the real classes if you prefer (which I do often).
  * Use AssertWasCalled instead of .Expect() on my mocks

I'll post more examples of this as they come up.
