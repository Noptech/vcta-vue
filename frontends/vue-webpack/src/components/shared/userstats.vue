<template>
  <div>
    <b-card :header="header">
      <table class="table table-hover">
        <thead>
        </thead>
        <tbody>
          <tr>
            <td>Username</td>
            <td>{{userInfo.username}}</td>
          </tr>
          <tr>
            <td>Full name</td>
            <td>{{userInfo.fullName}}</td>
          </tr>
          <tr>
            <td>Total distance</td>
            <td>{{userInfo.distance}}</td>
          </tr>
          <tr>
            <td>Number of trips</td>
            <td>{{userInfo.trips}}</td>
          </tr>
          <tr>
            <td>Cycling days</td>
            <td>{{userInfo.days}}</td>
          </tr>
          <tr>
            <td>Team</td>
            <td><router-link :to="{name: 'teamdetails', params: {id: userInfo.team}}">{{userInfo.teamName}}</router-link></td>
          </tr>
        </tbody>
      </table>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'userstats',
  props: [
    'header',
    'userInfo'
  ]
}
</script>

<style>

</style>
