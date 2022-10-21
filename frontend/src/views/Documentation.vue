<!--
Created by Nicolas Torquet at 12/07/2022
torquetn@igbmc.fr
Copyright: CNRS - INSERM - UNISTRA - ICS - IGBMC
CNRS - Mouse Clinical Institute
PHENOMIN, CNRS UMR7104, INSERM U964, Université de Strasbourg
Code under GPL v3.0 licence
-->
<template>
  <h1 class="title">Documentation</h1>

  <b-alert show class="info">
    You can find these descriptions <a href="https://livemousetracker.org/" target="_blank">here</a> and in the <a href="https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D" target="_blank">LMT publication</a>.<br />
    LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</a>.
  </b-alert>

  <b-container>
    <b-table-simple stripped hover small caption-top responsive>
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">Name</b-th>
          <b-th style="width: 10%">Representation</b-th>
          <b-th>Description</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr>
          <b-td>Total distance</b-td>
          <b-td></b-td>
          <b-td>
            Total distance in meter travelled by the focus animal during all the experiment.
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Single move</b-td>
          <b-td><img src="@\assets\img_moving.jpg" alt="moving" /></b-td>
          <b-td>
            The focal animal is moving (speed > 5 m/s) without being in contact with any other animal (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Move in contact</b-td>
          <b-td></b-td>
          <b-td>
           The focal animal is moving (speed > 5 m/s) while being in contact with another animal (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Stop isolated</b-td>
          <b-td></b-td>
          <b-td>
            The focal animal is resting (not moving) without being in contact with any other animal (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Rear isolated</b-td>
          <b-td><img src="@\assets\img_rearing.jpg" alt="rearing" /></b-td>
          <b-td variant="warning">
            The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Rear in contact</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Contact</b-td>
          <b-td><img src="@\assets\img_cct.jpg" alt="contact" /></b-td>
          <b-td>
            The focal animal is touching another individual (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Group of 2</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is touching one and only one other individual (total duration, number of events, mean duration of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Group of 3</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is touching two and only two other individuals (total duration, number of events, mean duration of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Nose-nose</b-td>
          <b-td><img src="@\assets\img_nose-nose.jpg" alt="nose-nose" /></b-td>
          <b-td>
            The focal animal is sniffing the nose of another animal (i.e., the nose is at a whisker distance from the nose of the other animal) (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Nose-anogenital</b-td>
          <b-td><img src="@\assets\img_nose-anogenital.jpg" alt="nose-anogenital" /></b-td>
          <b-td>
            The focal animal is sniffing the ano-genital region of another animal (i.e., the nose is at a whisker distance from the tail basis of the other animal) (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Side-side</b-td>
          <b-td><img src="@\assets\img_side-side.jpg" alt="side-side" /></b-td>
          <b-td>
            The flank of the focal animal is in contact with the flank of another animal; both animals head in the same direction (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Side-side head-to-tail</b-td>
          <b-td><img src="@\assets\img_side-side_opp.jpg" alt="side-side_opposite" /></b-td>
          <b-td>
            The flank of the focal animal is in contact with the flank of another animal; both animals head in opposite directions (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Train 2</b-td>
          <b-td><img src="@\assets\img_train2.jpg" alt="train 2" /></b-td>
          <b-td>
            The focal animal is moving (speed > 5 m/s) while sniffing the ano-genital region of another animal also moving (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Follow</b-td>
          <b-td></b-td>
          <b-td>
            The focal animal is walking in the path of another individual: the two animals are moving at a speed >5 cm/s, the angles between the two animals are less than 45° apart, and the mass centre of the follower (the focal animal) is within a follow zone of one mean body length of width and two mean body lengths of length (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Social approach</b-td>
          <b-td><img src="@\assets\img_soc_app.jpg" alt="social approach" /></b-td>
          <b-td>
            The focal animal gets closer to another one within a circular zone of 2 body lengths around the approached animal (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Approach contact</b-td>
          <b-td><img src="@\assets\img_app_cct.jpg" alt="approach contact" /></b-td>
          <b-td>
            The focal animal gets closer to another one within a circular zone of two body lengths around the approached animal; the approach ends by a contact between the two animals (total duration, number of events, mean duration of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Make group 3</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is joining a group of two animals to form a group of three animals in contact (number of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Make group 4</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is joining a group of three animals to form a group of four animals in contact (number of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td>Break contact</b-td>
          <b-td><img src="@\assets\img_break_cct.jpg" alt="break contact" /></b-td>
          <b-td>
            The focal animal is getting away (higher speed) from the animal it has been in contact with; the speed of the focal animal is higher than the speed of the other animal (number of events).
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Break group 3</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is leaving a group of three animals to leave a group of two animals in contact; the focal animal has the highest speed among the three animals in contact (number of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
        <b-tr>
          <b-td variant="warning">Break group 4</b-td>
          <b-td></b-td>
          <b-td variant="warning">
            The focal animal is leaving a group of four animals, that remain as a group of three animals in contact; the focal animal has the highest speed among the four animals in contact (number of events).<br />
            <b-icon-exclamation-triangle></b-icon-exclamation-triangle> <strong>This event has to be validated</strong>
          </b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>
  </b-container>

  <b-alert show class="info">
    For social events, we computed the variables either in general or separately according to the identity of the interacting individual. These behaviours are not exclusive: one animal can be involved in several of them simultaneously.
  </b-alert>
</template>




<script>
import {
  BIconExclamationTriangle
} from "bootstrap-icons-vue";

export default {
  name: "Documentation",
  components: {
    BIconExclamationTriangle,
  }
}
</script>

<style scoped>
.info {
  margin: auto;
  width: 100em;
}

table {
  margin: 2.5%;
  width: 95%;
}

</style>