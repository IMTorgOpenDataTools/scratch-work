<template>
    <h3>Domains to search:</h3>
    <form onsubmit="event.preventDefault();">
        <label for="url" >Enter url: </label>
        <input type="text" id="url" name="url" v-model="newUrl">
        <button @click="addItem">Add</button>
        <div v-for="url of urlList">
            <ul>
                <span>
                    {{ url }} <button @click="deleteItem(url)">x</button>
                </span>
            </ul>
        </div>
        <br><br>
        <button @click="postDomain">Submit</button>
    </form>
    <div v-for="item of results">
       <div v-html="item"></div>
    </div>
 </template>
    
<script>
export default{
    name:'BtnFetch',
    data(){
        return{
            defaultUrl: '<domain>',
            newUrl: '<domain>',
            urlList: [],
            results: []
        }
    },
    methods:{
        addItem(){
            this.urlList.push(this.newUrl)
            this.newUrl = this.defaultUrl
        },
        deleteItem(url){
            const idx = this.urlList.indexOf(url)
            if(idx > -1){
                this.urlList.splice(idx, 1)
            }
        },
        async getFAIL(){
            /*Connecting to pages from the browser is very restrictive*/
            const completeUrl = 'https://' + this.url    
            console.log(completeUrl)
            try {
                let resp = await fetch(completeUrl, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    mode: "cors", // no-cors, *cors, same-origin) 
                    //use 'cors' mode when you need to access data from a third-party API or server, and 'no-cors' mode when you don't need to access the response data
                    credentials: "omit",
                })
                console.log(resp.status)

                /*
                // Initialize the DOM parser
                var parser = new DOMParser();

                // Parse the text
                var doc = parser.parseFromString(html, "text/html");

                // You can now even select part of that html as you would in the regular DOM 
                // Example:
                // var docArticle = doc.querySelector('article').innerHTML;

                //console.log(doc);
                result = doc.URL
                console.log(result)
                */

                this.text = await resp.text()
            } catch (error) {
                console.error("Error:", error);
            }
        },
        async postDomain(){
            /*Post the domain to the API and receive the converted pdf.*/
            const completeUrl = 'http://127.0.0.1:5000/domain'    //window.location.href.split('/static')[0] + '/domain'
            console.log(completeUrl)
            try {
                let resp = await fetch(completeUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    mode: "cors",
                    credentials: "omit",
                    body: JSON.stringify({'domainUrl': this.urlList})
                })
                console.log(resp.status)
                const results = await resp.json()
                const display = []
                for(const [k,v] of Object.entries(results['results'])){
                    const href = resp['url'].split('/domain')[0] + '/' + v[1]
                    const assetHref = `<a href="${href}">${k}</a> result:${v[0]}`
                    display.push(assetHref)
                }
                Object.assign(this.results, display)



            } catch (error) {
                console.error("Error:", error);
            }
        }



    }
}


</script>