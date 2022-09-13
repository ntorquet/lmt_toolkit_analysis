<template>
  <h1 class="title">Documentation</h1>

  <b-alert show class="info">
    You can find these descriptions <a href="https://livemousetracker.org/" target="_blank">here</a> and in the <a href="https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D" target="_blank">LMT publication</a>.<br />
    LMT-toolkit uses the LMT-analysis code provided on GitHub <a href="https://github.com/fdechaumont/lmt-analysis" target="_blank">here</a>.
  </b-alert>

  <table class="table table-striped table-hover">
    <thead>
      <tr>
        <th style="width: 5%">Name</th>
        <th style="width: 10%">Representation</th>
        <th>Description</th>
      </tr>
    </thead>
    <tr>
      <td>Total distance</td>
      <td></td>
      <td>
        Total distance in meter travelled by the focus animal during all the experiment.
      </td>
    </tr>
    <tr>
      <td>Single move</td>
      <td><img src="@\assets\img_moving.jpg" alt="moving" /></td>
      <td>
        The focal animal is moving (speed > 5 m/s) without being in contact with any other animal (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Move in contact</td>
      <td></td>
      <td>
       The focal animal is moving (speed > 5 m/s) while being in contact with another animal (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Wall jumps</td>
      <td></td>
      <td>
        The focal animal is jumping against the wall (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Stop isolated</td>
      <td></td>
      <td>
        The focal animal is resting (not moving) without being in contact with any other animal (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Rear isolated</td>
      <td><img src="@\assets\img_rearing.jpg" alt="rearing" /></td>
      <td>
        The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Rear in contact</td>
      <td></td>
      <td>
        The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Contact</td>
      <td><img src="@\assets\img_cct.jpg" alt="contact" /></td>
      <td>
        The focal animal is touching another individual (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Group of 2</td>
      <td></td>
      <td>
        The focal animal is touching one and only one other individual (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Group of 3</td>
      <td></td>
      <td>
        The focal animal is touching two and only two other individuals (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Nose-nose</td>
      <td><img src="@\assets\img_nose-nose.jpg" alt="nose-nose" /></td>
      <td>
        The focal animal is sniffing the nose of another animal (i.e., the nose is at a whisker distance from the nose of the other animal) (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Nose-anogenital</td>
      <td><img src="@\assets\img_nose-anogenital.jpg" alt="nose-anogenital" /></td>
      <td>
        The focal animal is sniffing the ano-genital region of another animal (i.e., the nose is at a whisker distance from the tail basis of the other animal) (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Side-side</td>
      <td><img src="@\assets\img_side-side.jpg" alt="side-side" /></td>
      <td>
        The flank of the focal animal is in contact with the flank of another animal; both animals head in the same direction (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Side-side head-to-tail</td>
      <td><img src="@\assets\img_side-side_opp.jpg" alt="side-side_opposite" /></td>
      <td>
        The flank of the focal animal is in contact with the flank of another animal; both animals head in opposite directions (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Train 2</td>
      <td><img src="@\assets\img_train2.jpg" alt="train 2" /></td>
      <td>
        The focal animal is moving (speed > 5 m/s) while sniffing the ano-genital region of another animal also moving (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Follow</td>
      <td></td>
      <td>
        The focal animal is walking in the path of another individual: the two animals are moving at a speed >5 cm/s, the angles between the two animals are less than 45° apart, and the mass centre of the follower (the focal animal) is within a follow zone of one mean body length of width and two mean body lengths of length (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Social approach</td>
      <td><img src="@\assets\img_soc_app.jpg" alt="social approach" /></td>
      <td>
        The focal animal gets closer to another one within a circular zone of 2 body lengths around the approached animal (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Approach contact</td>
      <td><img src="@\assets\img_app_cct.jpg" alt="approach contact" /></td>
      <td>
        The focal animal gets closer to another one within a circular zone of two body lengths around the approached animal; the approach ends by a contact between the two animals (total duration, number of events, mean duration of events).
      </td>
    </tr>
    <tr>
      <td>Make group 3</td>
      <td></td>
      <td>
        The focal animal is joining a group of two animals to form a group of three animals in contact (number of events).
      </td>
    </tr>
    <tr>
      <td>Make group 4</td>
      <td></td>
      <td>
        The focal animal is joining a group of three animals to form a group of four animals in contact (number of events).
      </td>
    </tr>
    <tr>
      <td>Break contact</td>
      <td><img src="@\assets\img_break_cct.jpg" alt="break contact" /></td>
      <td>
        The focal animal is getting away (higher speed) from the animal it has been in contact with; the speed of the focal animal is higher than the speed of the other animal (number of events).
      </td>
    </tr>
    <tr>
      <td>Break group 3</td>
      <td></td>
      <td>
        The focal animal is leaving a group of three animals to leave a group of two animals in contact; the focal animal has the highest speed among the three animals in contact (number of events).
      </td>
    </tr>
    <tr>
      <td>Break group 4</td>
      <td></td>
      <td>
        The focal animal is leaving a group of four animals, that remain as a group of three animals in contact; the focal animal has the highest speed among the four animals in contact (number of events).
      </td>
    </tr>
  </table>

  <b-alert show class="info">
    For social events, we computed the variables either in general or separately according to the identity of the interacting individual. These behaviours are not exclusive: one animal can be involved in several of them simultaneously.
  </b-alert>
</template>




<script>
export default {
  name: "Documentation"
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