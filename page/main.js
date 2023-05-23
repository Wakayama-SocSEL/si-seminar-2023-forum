const messageList = new Vue({
    el: '#content',
    data: {
        messages: []
    },
    mounted: function() {
        fetch("http://localhost:8000/messages")
        .then(res => res.json())
        .then(data => messageList.messages = data);
    },
    methods: {
        updateMessage: function(){
            fetch("http://localhost:8000/messages")
            .then(res => res.json())
            .then(data => messageList.messages = data);
        }
    }
})

const submitForm = new Vue({
    el: '#submitForm',
    data: {
        ip_address: '',
        body: ''
    },
    async mounted() {
        fetch("https://ipinfo.io/ip")
        .then(res => res.text())
        .then(data => submitForm.ip_address = data);
    },
    methods: {
        submit: function(){
            const param = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    author: this.ip_address,
                    body: this.body
                })
            };
            fetch("http://localhost:8000/post/", param)
            .then(messageList.updateMessage());
        }
    }
})
