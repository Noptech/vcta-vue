<template>
  <div>
    <div v-if="dashboard.loading">Loading</div>
    <div class="row" v-if="!dashboard.loading">
      <div class="col-md-5">
        <userstats header="My Stats" :userInfo="dashboard.userInfo"></userstats>
        <teamrequests header="Sent team requests" :requests="requests"></teamrequests>
      </div>
      <div class="col-md-7">
        <tripscard :trips="dashboard.trips" :editable="true"></tripscard>
        <teammanagement></teammanagement>
      </div>
    </div>
  </div>
</template>

<script>
import userstats from '../components/shared/userstats.vue'
import teamrequests from '../components/dashboard/teamrequests.vue'
import teammanagement from '../components/dashboard/teammanagement.vue'
import tripscard from '../components/shared/tripscard.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'dashboard',
  computed: {
    ...mapGetters({
      dashboard: 'dashboard',
      requests: 'requests'
    })
  },
  created() {
    this.getDashboard()
  },
  methods: {
    ...mapActions([
      'getDashboard'
    ])
  },
  components: {
    userstats,
    teamrequests,
    tripscard,
    teammanagement
  }
}
</script>

<style lang="less">
.card {
  margin-bottom: 16px;
}
</style>
