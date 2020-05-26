import '@babel/polyfill'
import 'react-app-polyfill/ie11';
import FHIR from "fhirclient"
 // sets window.FHIR
import urlUtils from "./util/url";

import React from "react";
import ReactDOM from "react-dom";
import App from "./App.js";
console.log("completed imports");
// get the URL parameters received from the authorization server
const state = urlUtils.getUrlParameter("state"); // session key
const code = urlUtils.getUrlParameter("code"); // authorization code
console.log(state);
// load the app parameters stored in the session
const params = JSON.parse(sessionStorage[state]); // load app session
const tokenUri = params.tokenUri;
const clientId = params.clientId;
const secret = params.secret;
const serviceUri = params.serviceUri;
sessionStorage["serviceUri"] = serviceUri;
const redirectUri = params.redirectUri;
// This endpoint available when deployed in CRD server, for development we have
// the proxy set up in webpack.config.dev.js so the CRD server needs to be running
const FHIR_PREFIX = "../../crd/fhir/";
const FILE_PREFIX = "../../crd/"
var data = `code=${code}&grant_type=authorization_code&redirect_uri=${redirectUri}`;
// const data = new URLSearchParams();
// data.append("code", code);
// data.append("grant_type", "authorization_code");
// data.append("redirect_uri", redirectUri);
if (!secret) data += "&client_id=" + clientId;

const headers = {
  "Content-Type": "application/x-www-form-urlencoded"
};
if (secret) headers["Authorization"] = "Basic " + btoa(clientId + ":" + secret);

// obtain authorization token from the authorization service using the authorization code
const tokenPost = new XMLHttpRequest();
var auth_response;
tokenPost.open("POST", tokenUri);
tokenPost.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
tokenPost.onload = function() {
    if (tokenPost.status === 200) {
      try {
  
        auth_response = JSON.parse(tokenPost.responseText);
        console.log(auth_response);
      } catch (e) {
        const errorMsg = "Failed to parse auth response";
        document.body.innerText = errorMsg;
        console.error(errorMsg);
        return;
      }

      let appContext = {};
      try {
        const appString = decodeURIComponent(auth_response.appContext);
        // Could switch to this later
        appString.split("&").map((e)=>{
            const temp = e.split("=");
            appContext[temp[0]] = temp.slice(1).join("=");
        })
        // appContext = {
        //     template: appString.split("&")[0].split("=")[1],
        //     request: JSON.parse(appString.split("&")[1].split("=")[1].replace(/\\/g,"")),
        //   }
      } catch (e) {
        console.log(e);
        alert("error parsing app context, using default")
      }

      if (!appContext.hasOwnProperty("request")) {
        appContext = {
          template: "Questionnaire/HomeOxygenTherapy",
          request: '{\"resourceType\":\"DeviceRequest\",\"id\":\"265217\",\"meta\":{\"versionId\":\"2\",\"lastUpdated\":\"2020-04-29T15:51:47.000+00:00\",\"source\":\"#lJ1q5kx5cH5M3cz8\"},\"text\":{\"status\":\"generated\",\"div\":\"<div xmlns=\\\"http:\/\/www.w3.org\/1999\/xhtml\\\">This is a simple narrative with only plain text<\/div>\"},\"extension\":[{\"url\":\"http:\/\/build.fhir.org\/ig\/HL7\/davinci-crd\/R4\/ext-insurance.html\",\"valueReference\":{\"reference\":\"Coverage\/1489602\"}},{\"url\":\"http:\/\/mihin.org\/extension\/copyright\",\"valueString\":\"Copyright 2014-2020 Michigan Health Information Network Shared Services. Licensed under the Apache License, Version 2.0 (the \'License\'); you may not use this file except in compliance with the License. You may obtain a copy of the License at  http:\/\/www.apache.org\/licenses\/LICENSE-2.0.  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an \'AS IS\' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\"}],\"status\":\"completed\",\"intent\":\"original-order\",\"codeCodeableConcept\":{\"coding\":[{\"system\":\"https:\/\/bluebutton.cms.gov\/resources\/codesystem\/hcpcs\",\"code\":\"E0424\",\"display\":\"Stationary Compressed Gaseous Oxygen System, Rental\"}]},\"subject\":{\"reference\":\"Patient\/6\",\"display\":\"Katherine Elaine Taylor MD\"},\"authoredOn\":\"2020-04-08T11:00:00+00:00\",\"performer\":{\"reference\":\"Practitioner\/1\"},\"reasonCode\":[{\"coding\":[{\"system\":\"http:\/\/snomed.info\/sct\",\"code\":\"840544004\",\"display\":\"Suspected COVID-19\"}]}],\"insurance\":[{\"reference\":\"Coverage\/1489602\"}]}',
        }
      }

        var smart = FHIR.client({
        serverUrl: serviceUri,
        patientId: auth_response.patient,
        tokenResponse: {
            type: "bearer",
            access_token: auth_response.access_token,
            patient: auth_response.patient,
        }
        });
        let deviceRequestObj = JSON.parse(appContext.request.replace(/\\(.)/g, "$1"));
        try {
          deviceRequestObj.text.div = deviceRequestObj.text.div.replace(/\+/g, " ");
        } catch (e) {}
        
        ReactDOM.render(
        <App
          FHIR_PREFIX={FHIR_PREFIX}
          FILE_PREFIX={FILE_PREFIX}
          questionnaireUri={appContext.template}
          smart={smart}
          deviceRequest={deviceRequestObj}
        />,
        document.getElementById("root")
        );
        console.log(auth_response);
        const patientId = auth_response.patient;
        if (patientId == null) {
        const errorMsg = "Failed to get a patientId from the app params or the authorization response.";
        document.body.innerText = errorMsg;
        console.error(errorMsg);
        return;
        }
        return patientId;
    } else {
      const errorMsg = "Token post request failed. Returned status: " + tokenPost.status;
      document.body.innerText = errorMsg;
      console.error(errorMsg);
      return;
    }
    return patientId;

};
tokenPost.send(data);


