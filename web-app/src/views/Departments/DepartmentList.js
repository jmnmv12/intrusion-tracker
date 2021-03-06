import React, { Component } from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { BrowserRouter as Router, Switch, Redirect } from "react-router-dom";

// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { withStyles } from "@material-ui/core/styles";
import Icon from "@material-ui/core/Icon";

import Button from "components/CustomButtons/Button.js";

// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Tasks from "components/Tasks/Tasks.js";
import CustomTabs from "components/CustomTabs/CustomTabs.js";
import Danger from "components/Typography/Danger.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";

import { bugs, website, server } from "variables/general.js";

import DepartmentInfo from "./DepartmentInfo";

import global from "../../variables/global";
import baseURL from "../../variables/baseURL";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";

export class DepartmentList extends Component {
  state = {
    isLoaded: false,
    token_expired: false,
    departments: [],
    redirect: false,
    id: null,
    department: null
  };

  // Calls to our API
  componentDidMount = () => {
    global = JSON.parse(localStorage.getItem('global'))

    //Get a list of departments
    fetch(baseURL + "api/v1/departments", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: global["token"]
      }
    })
      .then(response => {
        if (response.ok)
            return response.json()
        else if (response.status == "401")
        this.setState({
          token_expired: true
        });
        else {
            throw new Error(response.status);
        }
      })
      .then(data => {
        this.setState({
          departments: data,
          isLoaded: true
        });
      })
      .catch(error => {
        console.log("error: " + error);
      });
  };

  go_to_more = (id,name) => {
    this.setState({
      id: id,
      department: name
    });
  };

  //Go back to login
  renderRedirectLogin = () => {
    if (this.state.token_expired) {
      localStorage.setItem('global', null);
      return <Redirect to="/login" />;
    }
  };

  render() {
    const { classes } = this.props;
    const { isLoaded, departments, id, department } = this.state;

    if (!isLoaded) {
      return (
        <div>
          {this.renderRedirectLogin()}
          <h2>Loading...</h2>
        </div>
      );
    } else if (id == null) {
      return (
        <div>
          <GridContainer>
            {departments.map(department => (
              <GridItem xs={12} sm={6} md={3} key={department.id}>
                <Card>
                  <CardHeader color="warning" stats icon>
                    <CardIcon color="warning">
                      <h4>
                        <strong>{department.id}</strong>
                      </h4>
                    </CardIcon>
                    <p className={classes.cardCategory}>Department name</p>
                    <h3 className={classes.cardTitle}>
                      <strong>{department.departmentName}</strong>
                    </h3>
                  </CardHeader>
                  <CardFooter stats>
                    <div className={classes.stats}>
                      <Button
                        color="warning"
                        onClick={() => this.go_to_more(department.id,department.departmentName)}
                      >
                        <strong>More info</strong>
                      </Button>
                    </div>
                  </CardFooter>
                </Card>
              </GridItem>
            ))}
          </GridContainer>
        </div>
      );
    } else {
      return <DepartmentInfo id={id} name={department} classes={classes} />;
    }
  }
}

export default withStyles(styles)(DepartmentList);
