import {faker} from '@faker-js/faker';
import {addDays, randomIntFromInverval} from './utils.js';
import { useLifecycle, useProject } from '../main.js';




// Lifecycle and Steps

let step_Prospect = {
    Name:'prospect',
    DurationBizDays: 3,
    Order:0,
    Placeholder:[], 
    EmailForm: ``
}

let step_Lead = {
    Name:'lead',
    DurationBizDays: 7, 
    Order:1, 
    Placeholder: [`<CONTACT_FULLNAME>`, `<CONTACT_REFERREDBY>`, `<PRODUCT_NAME>`, `<ACCOUNT_FULLNAME>`],
    EmailForm: `
<CONTACT_FULLNAME>,

You were referred to me by <CONTACT_REFERREDBY>, and I'd like to schedule you for a demo of the <PRODUCT_NAME> app.

Please let me know what time works best for you.

Respectfully,
<ACCOUNT_FULLNAME>
`}

let step_Onboarded =  {
    Name:'onboarded',
    DurationBizDays: 14, 
    Order:2, 
    Placeholder: [`<CONTACT_FULLNAME>`,`<PRODUCT_NAME>`, `<ACCOUNT_FULLNAME>`],
    EmailForm: `
<CONTACT_FULLNAME>,

Thanks again for taking the time to try <PRODUCT_NAME>!  

If there is any problem or functionality that is unclear, please let me know.  I try to be
responsive to your needs.  Typically, we can have updates and fixes completed in a week.

Respectfully,
<ACCOUNT_FULLNAME>
`}

let step_Followup = {
    Name: 'followup',
    DurationBizDays: 7,
    Order: 3, 
    Placeholder: [`<CONTACT_FULLNAME>`,`<PRODUCT_NAME>`, `<ACCOUNT_FULLNAME>`],
    EmailForm:`
<CONTACT_FULLNAME>,

Hi, I was wondering if you had a chance to try the <PRODUCT_NAME> tool and had an initial feelings?

Also, if you could provide the names of two other people who might be interested, please let me know
so that others can try it out.

Respectfully,
<ACCOUNT_FULLNAME>
`}

let step_Intention = {
    Name: 'intention',
    DurationBizDays: 14,
    Order: 4, 
    Placeholder: [`<CONTACT_FULLNAME>`,`<PRODUCT_NAME>`, `<ACCOUNT_FULLNAME>`],
    EmailForm:`
<CONTACT_FULLNAME>,

Thanks for taking the time to try <PRODUCT_NAME>.  I'm hoping to get your feedback and your intention to using 
the product, in the future.

Respectfully,
<ACCOUNT_FULLNAME>
`}

export const defaultSteps = [
  step_Prospect,
  step_Lead,
  step_Onboarded,
  step_Followup,
  step_Intention
]

export const defaultLifecycle = {
    Name: 'default',
    LifecycleStep: []
}





// Projects
export const testProjects = []
var i = 0;
while(i < 3){
    const dtBegin = faker.date.betweens({from: '2020-01-01T00:00:00.000Z', to:'2023-01-01T00:00:00.000Z', count:1})[0]
    const dtEnd = addDays(dtBegin, randomIntFromInverval(100,200))
    const project = {
        Name: faker.commerce.productName(),
        Status: 'active',
        Category: faker.commerce.product(),
        Startdate: new Date(dtBegin),
        Enddate: new Date(dtEnd),
        Lifecycle: defaultLifecycle.Name,
        Repos: faker.internet.url()
    }
    testProjects.push(project)
    i++
}

// Contacts
export const testContacts = []
i = 0;
while(i < 10){
    const projects = randomIntFromInverval(0, testProjects.length-1) //TODO:add multiple projects
    const contact = {
        Fullname: faker.person.fullName(),
        Title: faker.person.jobTitle(),
        Email: faker.internet.email(),
        Number: faker.phone.number(),
        Office: faker.commerce.department(),
        Firm: faker.company.name(),
        Projects: [testProjects[projects].Name],
        Statuses: []
    }
    const numberOfInteractions = randomIntFromInverval(1,5)
    const interactions = []
    let j = 0
    while(j < numberOfInteractions){
        const interaction = {
            LifecycleStep: defaultSteps[randomIntFromInverval(0,3)].Name,
            Participants: [contact.Fullname],
            Datetime: new Date(),
            Comments: faker.lorem.paragraph(),
        }
        interactions.push(interaction)
        j++
    }
    const numberOfUseCases = randomIntFromInverval(2,3)
    const usecases = []
    j = 0
    while(j < numberOfUseCases){
        const usecase = {
            Role: faker.person.jobTitle(),
            Use: faker.lorem.sentence(),
            PainPoint: faker.lorem.sentence()
        }
        usecases.push(usecase)
        j++
    }

    let referredBy = ''
    if(testContacts.length > 2){
        const chooseFromContacts = randomIntFromInverval(0,testContacts.length-1)
        referredBy = testContacts[chooseFromContacts]
    } else {
        referredBy = faker.person.fullName()
    }
    const status = {
        Person: contact.Fullname,
        Project: contact.Projects[0],
        ReferredBy: '',     //TODO:applying referredBy errors
        CurrentLifecycleStep: defaultSteps[randomIntFromInverval(3,defaultSteps.length-1)].Name,
        Interactions: interactions,
        UseCases: usecases
    }
    contact.Statuses.push(status)


    testContacts.push(contact)
    i++
}

const testAccount = {
    Fullname: faker.person.fullName()
}

// Populate
export function populateAccountTestData(useProject){
    // Populate tables with test data
      useProject.save({
        Fullname: testAccount.Fullname,
        });
}

export function populateProjectTestData(useProject, lifecycleId){
    // Populate tables with test data
    for(const project of testProjects){
      useProject.save({
          Name: project.Name,
          Status: project.Status,
          Category: project.Category,
          StartDate: project.Startdate,
          EndDate: project.Enddate,
          LifecycleId: lifecycleId,
          Repos: project.Repos
        });
    }
}

export function populateContactTestData(usePerson, project, referredBy){
    // Populate tables with test data
    for(const contact of testContacts){
        //get random person for referredby
        const persons = usePerson.all()
        let refId = null
        if( persons.length > 0){
            const int = randomIntFromInverval(0,persons.length-1)
            refId = persons[int].id
        }
        //get step
        const lc = useLifecycle.all()
        const selected_lc = lc.filter(item => item.id == project.LifecycleId)[0]
        const selected_step = selected_lc.LifecycleStep[randomIntFromInverval(0, selected_lc.LifecycleStep.length-1)]
        
        const dt = faker.date.betweens({from: '2020-01-01T00:00:00.000Z', to:'2023-01-01T00:00:00.000Z', count:1})[0]
        contact.Statuses
        usePerson.save({
            Fullname: contact.Fullname,
            Title: contact.Title,
            Email: contact.Email,
            Number: contact.Number,
            Office: contact.Office,
            Firm: contact.Firm,
            Statuses: [{
                ProjectId: project.id,
                RefId: refId,
                LifecycleSteps: [{
                    LifecycleStepId: selected_step.id,
                    StatusDate: new Date(dt)
                }],
            }]
            // collect with repos
            //...TODO
      });
    }
  }