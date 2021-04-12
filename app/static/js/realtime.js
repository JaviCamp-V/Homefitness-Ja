


const app = Vue.createApp({
    data() {
        return {

        }
    }
});


const Bcurls = {
    name: 'Home',
    template: `
    <div class="webcam-box">
    </div>
    <div class="eval-box">
       
    </div>
    `,
    data() {
        return {
            reps:0,
            correction:[],
        }
    },
    methods: {

    }   
};



const NotFound = {
    name: 'NotFound',
    template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
    data() {
        return {}
    }
};

// Define Routes
const routes = [
    { path: "/RealTime/", component: Bcurls },

    // Put other routes here

    // This is a catch all route in case none of the above matches
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes, // short for `routes: routes`
});

app.use(router);

app.mount('#app');