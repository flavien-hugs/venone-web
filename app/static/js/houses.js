var app = Vue.createApp({

	data() {
		return {
			houses: [],
		};
	},

    async mounted() {
        await this.getHouses();
    },

    methods: {
    	async getHouses() {
        	try {
        		const houseURL = `https://g.venone.app/api/available-houses/`;

        		const response = await fetch(houseURL, {
        			method: "GET",
        			headers: {
        				"Content-type": "application/json",
        			},
        		});

        		if (response.status == 200) {
        			const data = await response.json();
        			this.houses = data.houses;
        		} else {
        			throw new Error("NETWORK RESPONSE ERROR");
        		}
        	} catch (error) {
        		console.error("FETCH ERROR:", error);
        	}
    	},
    }
});

app.component('house-list', {
  	props: ['houses'],
  	template: `
	    <article class="col-6" v-for="house in houses" :key="house.house_id">
			<div class="card shadow p-2">
				<div class="row g-0">
					<div class="col-md-5">
						<img loading="lazy" class="rounded-2" src="{{ url_for('static', filename='img/logo/logo.png') }}" alt="card image">
					</div>

					<div class="col-md-7">
						<div class="card-body">
							<div class="d-flex justify-content-between align-items-center mb-2">
								<a href="#" class="badge bg-primary mb-2 mb-sm-0">{{ house.house_type }}</a>
							</div>
							<h1 class="card-title fs-5 mb-3"><a href="#">The Complete Digital Marketing Course</a></h1>
							<p class="text-truncate-2">Satisfied conveying a dependent contented he gentleman agreeable do be. dependent contented he</p>
							<ul class="list-inline mb-3">
								<li class="list-inline-item h6 fw-light mb-1 mb-sm-0"><i class="far fa-clock text-danger me-2"></i>6h 56m</li>
								<li class="list-inline-item h6 fw-light mb-1 mb-sm-0"><i class="fas fa-table text-orange me-2"></i>82 lectures</li>
								<li class="list-inline-item h6 fw-light"><i class="fas fa-signal text-success me-2"></i>Beginner</li>
							</ul>
							<div class="d-sm-flex justify-content-sm-between align-items-center">
								<div class="d-flex align-items-center">
									<div class="avatar">
										<img loading="lazy" class="avatar-img rounded-circle" src="{{ url_for('static', filename='img/logo/favicon.png') }}" alt="avatar">
									</div>
								</div>               
							</div>
						</div>
					</div>
				</div>
			</div>
		</article>
  	`
});

app.mount("#housesApp");