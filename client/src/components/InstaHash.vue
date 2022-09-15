<template>
    <div class="container">

        <div>
            <b-modal size="lg" id="modal-scrollable" centered  hide-footer="true">
                <b-container>
                    <div style="height: 500px;" class="row">
                        <div class="col">
                            <img max-width="300px" width="100%" v-bind:src="'data:image/jpeg;base64,'+selectedPost.img_bin" />
                        </div>
                        <div class="col h-100 d-inline-block overflow-auto">
                            <div class="row">
                                <b>id: </b><p v-text="selectedPost.id"></p>
                            </div>
                            <div class="row">
                                <b>shortcode: </b><p v-text="selectedPost.shortcode"></p>
                            </div>
                            <div class="row">
                                <b>type: </b><p v-text="selectedPost.type"></p>
                            </div>
                            <div class="row">
                                <b>is_video: </b><p v-text="selectedPost.is_video"></p>
                            </div>
                            <div class="row">
                                <b>dimension: </b><p v-text="selectedPost.dimension"></p>
                            </div>
                            <div class="row">
                                <b>display_url: </b><p v-text="selectedPost.display_url"></p>
                            </div>
                            <div class="row">
                                <b>thumbnail_src: </b><p v-text="selectedPost.thumbnail_src"></p>
                            </div>
                            <div class="row">
                                <b>owner: </b><p v-text="selectedPost.owner"></p>
                            </div>
                            <div class="row">
                                <b>description: </b><p v-text="selectedPost.description"></p>
                            </div>
                            <div class="row">
                                <b>comments: </b><p v-text="selectedPost.comments"></p>
                            </div>
                            <div class="row">
                                <b>likes: </b><p v-text="selectedPost.likes"></p>
                            </div>
                            <div class="row">
                                <b>comments_disabled: </b><p v-text="selectedPost.comments_disabled"></p>
                            </div>
                            <div class="row">
                                <b>taken_at_timestamp: </b><p v-text="selectedPost.taken_at_timestamp"></p>
                            </div>
                            <div class="row">
                                <b>hashtags: </b>
                                <ul>
                                    <li v-for="(ht, index) in selectedPost.hashtags"  :key="index"><p v-text="ht"></p></li>
                                </ul>
                            </div>
                            <div class="row">
                                <b>mentions: </b>
                                <ul>
                                    <li v-for="(ht, index) in selectedPost.mentions"  :key="index"><p v-text="ht"></p></li>
                                </ul>
                            </div>
                            <div class="row">
                                <b>hashtag: </b><p v-text="selectedPost.hashtag"></p>
                            </div>
                            <div class="row">
                                <b>cursor: </b><p v-text="selectedPost.cursor"></p>
                            </div>
                            <div class="row">
                                <b>scraped_timestamp: </b><p v-text="selectedPost.scraped_timestamp"></p>
                            </div>
                        </div>
                    </div>
                </b-container>
            </b-modal>
        </div>

        <div class="row">
            <div class="col">
                <h1>InstaHash</h1>
                <hr>
                <br>
                <div class="row w-50">
                    <b-form @submit="onSubmit">
                        <b-form-group id="search-group" label="Search:" label-for="hashtag-search-field">
                            <b-form-input list="input-list" id="hashtag-search-field" type="text" required v-model="ht"
                                placeholder="Hashtag">
                            </b-form-input>
                            <b-form-datalist id="input-list" :options="htList"></b-form-datalist>
                        </b-form-group>
                        <b-form-group id="dp1-group" label="Pick date range:" label-for="dp1">
                            <date-picker type="date" range id="dp1" v-model="dateRange" value-type="format" format="X"
                                title-format="YYYY-MM-DD" :default-value="new Date()" :disabled-date="setMinMax">
                            </date-picker>
                        </b-form-group>
                        <br>
                        <b-button type="submit" variant="primary">
                            Search
                        </b-button>
                    </b-form>
                </div>
            </div>
        </div>
        <br>
        <br>

        <!-- Main content grid -->
        <div class="row">
            <div class="col">
                <div class="row" v-for="(p1, index) in chunkedPosts"  :key="index">
                    <div class="col" v-for="(p2, index2) in p1"   :key="index2">
                        <b-card 
                            v-on:click="loadModal(index*3 + index2)"
                            overlay
                            v-bind:img-src="'data:image/jpeg;base64,'+p2.img_bin"
                            img-alt="Image"
                            img-top
                            style="max-width: 20rem;"
                            class="mb-2">
                        </b-card>
                    </div> 
                </div>
            </div>
        </div>
        <div style="padding:15px" class="d-flex justify-content-center">
            <b-button type="button" class="btn w-25" v-if="loadMoreVis" @click="load_posts" variant="primary">Load More</b-button>
        </div>
    </div>

</template>

<script>
import axios from 'axios';
import chunk from 'chunk';
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';

export default {
    components: { DatePicker },
    data() {
        return {
            dateRange: [],
            posts: [],
            chunkedPosts: [],
            ht: '',
            payload: {},
            selectedPost: 0,
            htList: [],
            globalmin: new Date(),
            globalmax: new Date(),
            loadMoreVis: false,
            output: '',
        };
    },
    methods: {
        getPosts(payload) {
            this.output = 'getposts';
            const path = 'http://localhost:5000/posts';
            axios.post(path, payload)
                .then((res) => {
                    this.posts = res.data.posts;
                    this.chunkedPosts = chunk(this.posts, 3);
                    this.loadMoreVis = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        onSubmit(evt) {
            evt.preventDefault();
            if(this.dateRange.length != 0 && this.dateRange[0] != null) {
                this.payload = {
                    ht: this.ht,
                    t1: parseInt(this.dateRange[0]),
                    t2: parseInt(this.dateRange[1]),
                };
            } else {
                this.payload = {
                    ht: this.ht,
                    t1: 0,
                    t2: 0,
                };
            }
            this.getPosts(this.payload);

        },
        loadModal(index) {
            this.selectedPost = this.posts[index];
            this.$bvModal.show('modal-scrollable');
        },
        load_posts() {
            const path = 'http://localhost:5000/loadposts';
            axios.post(path)
                .then((res) => {
                    this.posts = this.posts.concat(res.data.posts);
                    this.chunkedPosts = chunk(this.posts, 3);
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getMinMax() {
            const path = 'http://localhost:5000/minmax';
            axios.get(path)
                .then((res) => {
                    this.htList = res.data.ht_list;
                    this.globalmax = new Date(res.data.global_max * 1000);
                    this.globalmin = new Date(res.data.global_min * 1000);
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        setMinMax(date) {
            return date < new Date(this.globalmin) || date > new Date(this.globalmax);
        },
    },
    created() {
        this.getMinMax();
    },
};
</script>
