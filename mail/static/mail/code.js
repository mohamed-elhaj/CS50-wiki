document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // document.querySelector("#mail-container").onclick = view_mail(71);
    document.querySelector("form").onsubmit = send_mail;


    // display none for email view by default
    document.querySelector("#email-view").style.display = 'none';
    
    // By default, load the inbox
    load_mailbox('inbox');
  });
  
  
  function compose_email() {
  
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  
  function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
  
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
    // Show the content of the mailbox
  
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      // display the data
      emails.forEach(email => display_email(email, mailbox));
      
    });
    
  }
  
  function display_email(email, mailbox) {
    const email_id = email.id
    const sender = email.sender;
    const recipient = email.recipients[0];
    const subject = email.subject;
    const body = email.body;
    const time = email.timestamp;
    // console.log(sender, recipient, subject, time)
  
    // Create a div to contain the fields
    const mailContainer = document.createElement('div');
    mailContainer.className = 'row'; // to style it using bootstrap
    mailContainer.id = 'mail-container';
  
    // Color of mailContainer
    if (email.read & mailbox === 'inbox')  {
      mailContainer.style.backgroundColor = 'whitesmoke';
    } else {
      mailContainer.style.backgroundColor = 'white';
    }

    // Create an empty div to contain either sender or reciepients
    const emailDiv = document.createElement('div');
    emailDiv.className = 'col-lg-4 col-sm-12';
    emailDiv.id = 'email-div';
  
    // Bug in here
    if (mailbox === "inbox") {
      emailDiv.innerHTML = sender;
    }else {
      emailDiv.innerHTML = recipient;
    }
    const mailSubject = document.createElement('div');
    mailSubject.className = 'col-lg-3 col-sm-12';
    mailSubject.id = 'email-subject';
    mailSubject.innerHTML = subject;
    
    const timeStamp = document.createElement('div');
    timeStamp.className = 'col-lg-3 col-sm-12';
    timeStamp.id = 'email-time';
    timeStamp.innerHTML = time;    

    // Add archive button for inbox mails
    
    
    mailContainer.append(emailDiv);
    mailContainer.append(mailSubject);
    mailContainer.append(timeStamp);
    
    // console.log(mailContainer);
    if (mailbox !== "sent") {
      // Create a button
      const button = document.createElement('i');
      button.className = "fas fa-archive";
      button.id = "archive";
      mailContainer.append(button);
      button.addEventListener('click', () => {
        archive(email_id, email.archived);
        window.location.reload();
      })
    }

    const mailView = document.querySelector('#emails-view');
    mailView.appendChild(mailContainer);

    // View email content when clicking
    // Took days to write this :)
    emailDiv.addEventListener('click', () => {
      view_email(email_id);
    });
    mailSubject.addEventListener('click', () => {
      view_email(email_id);
    });
    timeStamp.addEventListener('click', () => {
      view_email(email_id);
    });
    
  
  }
  
  
  function send_mail() {
  
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
      localStorage.clear();
      load_mailbox('sent');
      window.location.reload;
      return false;
  }

function view_email(email_id) {
  // document.querySelector("#mail-container").querySelectorAll("div")[3].id

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  const from = document.querySelector('.from-data');
  const to = document.querySelector('.to-data');
  const subject = document.querySelector('.subject-data');
  const time = document.querySelector('.time-data');
  const body = document.querySelector('.body-data');
  const reply_button = document.querySelector('#reply');
  

  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    // display the data
    
    // Add data to the fields
    from.innerHTML = email.sender;
    to.innerHTML = email.recipients[0];
    subject.innerHTML = email.subject;
    time.innerHTML = email.timestamp;
    body.innerHTML = email.body;
    reply_button.addEventListener("click", () => {
      reply(email);
    })

    mark_as_read(email_id)
  });


  }; 

function mark_as_read(email_id) {
  fetch(`emails/${email_id}`, {
    method: "PUT",
    body: body=JSON.stringify({
      read: true
    })
  })
}


function archive(email_id, current_value) {
  // Add or remove the element from archive
  const newValue = !current_value
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: newValue
    })
  })
}


function reply(email) {
  compose_email()

  // The recipient will be the sender in this case who is the current user
  document.querySelector("#compose-recipients").value = email.sender;


  if (email.subject.indexOf("Re: ") === -1 ){
    // if "Re: " is not existed, add it
    email.subject = "Re: " + email.subject;
  }

  // Add the value of the subject to the compose-subject field
  document.querySelector("#compose-subject").value = email.subject;

  
  email.body = `\n\nOn ${email.timestamp} ${email.sender} Wrote:\n ${email.body}`;
  document.querySelector("#compose-body").value = email.body;
  



}