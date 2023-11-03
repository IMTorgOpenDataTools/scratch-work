import { defineStore } from 'pinia'

const DisplayStore = defineStore('display',{
    state: () => {
        return {
            //Global
            populateDefault: true,
            populateTestData: true,
            viewCount: 0,
            viewSelection: {value: '1', text: 'Project', path:'ProjectPage'},
            options:[
                {value: '1', text: 'Project', path:'ProjectPage'},
                {value: '2', text: 'Contact', path:'ContactPage'},
                {value: '3', text: 'Lifecycle', path:'LifecyclePage'},
              ],
            projectSelection: {},

            //Project
            project: {
                initialCategory: 'Software',
                initialStatus: 'Active',
                initialStartDate: new Date(), 
                initialLifecycle: 'default',
                availableCategory: ['Software', 'Hardware'],
                availableStatus: ['Active', 'Delayed', 'Complete']
            }
        }
    }
})

export default DisplayStore