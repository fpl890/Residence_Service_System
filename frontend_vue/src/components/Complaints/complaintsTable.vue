<template>
  <table class="table">
    <thead class="table-secondary">
      <tr>
        <th>Complaint ID</th>
        <th>Student ID</th>
        <th>Staff ID</th>
        <th>Description</th>
        <th>Resolution Description</th>
        <th>Submission Date</th>
        <th>Date Resolved</th>
        <th>Status</th>
        <th>Urgency Rating</th>
        <th v-if="['staff', 'admin'].includes(userRole)"></th>
      </tr>
    </thead>
    <tbody>
      <complaint
        v-for="complaint in complaints"
        :key="complaint"
        :complaint="complaint"
        :staff="staff"
      ></complaint>
    </tbody>
  </table>
</template>

<script>
import complaint from "@/components/Complaints/complaint";
import axios from "axios";

export default {
  components: {
    complaint,
  },
  data() {
    return {
      complaints: [],
      url: "",
      staff: [],
    };
  },
  mounted() {
    let role = this.$store.state.role;
    let userID = this.$store.state.user.user_id;

    if (role == "student") {
      this.url = "students/" + userID + "/complaints/";
    } else if (role == "staff") {
      this.url = "staff/" + userID + "/complaints/";
    } else {
      this.url = "complaints/";
    }

    axios
      .get(this.url)
      .then((response) => {
        this.complaints = response.data;
      })
      .catch((error) => {
        console.log(error);
      });

    if (["admin"].includes(role)) {
      axios
        .get("staff/?general=true")
        .then((response) => {
          this.staff = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
  computed: {
    userRole: function () {
      return this.$store.state.role;
    },
  },
};
</script>

<style></style>
