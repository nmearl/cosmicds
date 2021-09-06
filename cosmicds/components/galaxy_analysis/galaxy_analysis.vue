<template>
  <span>
    <v-container>
      <v-row>
        <v-col cols="3">
          <v-btn
            block
            class="mb-4"
            :disabled="state.adddata_disabled"
            @click="state.next1_disabled = false"
            color="primary"
          >
            <v-icon left dark> mdi-plus </v-icon>
            Add Data
          </v-btn>
          <div color="green" class="text-body-2">
            You can add your data to the plot after you select a galaxy below,
            and then estimate the distance and measure the velocity of that
            galaxy.
          </div>
        </v-col>
        <v-col>
          <v-lazy>
            <jupyter-widget :widget="viewers.hub_const_viewer"></jupyter-widget>
          </v-lazy>
          <todo-alert>
            When students add velocity and distance measurements, they will be
            plotted here. (No data will be displayed to start. Points populate
            the plot as students measure and commit them.)
          </todo-alert>
        </v-col>
      </v-row>
    </v-container>
    <v-card color="blue lighten-5" class="" outlined>
      <v-tabs v-model="state.col_tab_model" centered>
        <v-tab key="gal-dist">
          <v-icon left> mdi-ruler </v-icon>
          Estimate Distance
        </v-tab>
        <v-tab key="gal-vel">
          <v-icon left> mdi-speedometer </v-icon>
          Measure Velocity
        </v-tab>
        <v-tab-item key="gal-dist">
          <v-container>
            <v-row>
              <!-- This WWT viewer widget allows user to select a galaxy; galaxy positions plotted by RA/Dec.
                              It will zoom in to chosen galaxy & put controls/instructions on screen. -->
              <!-- viewers.wwt_viewer doesn't need to be prepended with "state" because it comes from "Application" in app.py, not "ApplicationState"-->
              <v-col cols="12" md="7">
                <jupyter-widget :widget="viewers.wwt_viewer"></jupyter-widget>
              </v-col>

              <!-- Callout to select galaxy / info about selected galaxy -->
              <v-col cols="12" md="5">
                <v-alert
                  class="mb-4"
                  border="left"
                  colored-border
                  color="indigo"
                  elevation="2"
                >
                  Pan the sky and select one of the galaxies to measure.
                  <div class="text-center mt-4">
                    <v-btn
                      class="white--text"
                      color="purple darken-2"
                      @click="
                        state.gal_snackbar = 0;
                        state.dist_snackbar = 0;
                        state.marker_snackbar = 0;
                        state.vel_snackbar = 0;
                        state.data_ready_snackbar = 0;
                        state.gal_snackbar = 1;
                        state.gal_selected = 1;
                        state.haro_on = 'd-block';
                      "
                    >
                      select galaxy
                    </v-btn>
                  </div>
                </v-alert>
                <div :class="state.haro_on">
                  <v-card color="indigo lighten-5">
                    <v-card-title>Haro 11</v-card-title>
                    <v-card-text>
                      <v-divider></v-divider>
                      <v-list color="indigo lighten-5">
                        <v-list-item-content>
                          <v-list-item-title
                            >Irregular galaxy</v-list-item-title
                          >
                          <v-list-item-subtitle>type</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-content>
                          <v-list-item-title
                            >100,000 light years</v-list-item-title
                          >
                          <v-list-item-subtitle
                            >assumed size</v-list-item-subtitle
                          >
                        </v-list-item-content>
                        <v-list-item-content>
                          <v-list-item-title>568 pixels</v-list-item-title>
                          <v-list-item-subtitle
                            >height of display</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-list>
                      <v-divider></v-divider>
                      <v-text-field
                        :value="state.galaxy_dist"
                        label="Estimated Distance"
                        hint="click button below"
                        persistent-hint
                        color="purple darken-2"
                        class="mt-8 mb-4"
                        suffix="Mpc"
                        outlined
                        readonly
                        dense
                      ></v-text-field>
                      <v-btn
                        block
                        color="purple darken-2"
                        dark
                        class="px-auto"
                        max-width="100%"
                        @click="
                          state.dist_measured = 1;
                          state.gal_snackbar = 0;
                          state.dist_snackbar = 0;
                          state.marker_snackbar = 0;
                          state.vel_snackbar = 0;
                          state.data_ready_snackbar = 0;
                          state.vel_measured == 1
                            ? (state.data_ready_snackbar = 1)
                            : (state.dist_snackbar = 1);
                          state.adddata_disabled =
                            state.vel_measured == 1 ? false : true;
                          state.galaxy_dist =
                            Math.floor(Math.random() * 450) + 50;
                        "
                      >
                        estimate
                      </v-btn>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>

        <v-tab-item key="gal-vel">
          <v-container>
            <v-row>
              <v-col cols="12" md="8" class="align-stretch">
                <v-card min-height="300px" height="100%" class="pa-5">
                  TO DO: learn how to import Spectrum Lab .js code here.
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-alert
                  border="left"
                  colored-border
                  color="indigo"
                  elevation="2"
                  clas="mb-12"
                >
                  Drag the marker across the spectrum to measure the H-&#x3B1;
                  wavelength.
                  <div class="text-center mt-4">
                    <v-btn
                      :disabled="!state.gal_selected"
                      class="white--text"
                      color="purple darken-2"
                      @click="
                        state.gal_snackbar = 0;
                        state.dist_snackbar = 0;
                        state.marker_snackbar = 0;
                        state.vel_snackbar = 0;
                        state.data_ready_snackbar = 0;
                        state.marker_snackbar = 1;
                        state.marker_set = 1;
                        state.marker_on = 'd-block';
                      "
                    >
                      set marker
                    </v-btn>
                  </div>
                </v-alert>

                <div>
                  <v-card
                    color="indigo lighten-5"
                    clas="mb-4"
                    :disabled="!state.marker_set"
                  >
                    <v-card-text>
                      <v-text-field
                        :value="state.galaxy_vel"
                        label="Calculated Velocity"
                        hint="click button below"
                        persistent-hint
                        color="purple darken-2"
                        class="mb-4"
                        suffix="km/s"
                        outlined
                        readonly
                        dense
                      ></v-text-field>
                      <v-btn
                        block
                        color="purple darken-2"
                        class="px-auto"
                        max-width="100%"
                        dark
                        @click="
                          state.gal_snackbar = 0;
                          state.dist_snackbar = 0;
                          state.marker_snackbar = 0;
                          state.vel_snackbar = 0;
                          state.data_ready_snackbar = 0;
                          state.vel_measured = 1;
                          state.dist_measured == 1
                            ? (state.data_ready_snackbar = 1)
                            : (state.vel_snackbar = 1);
                          state.adddata_disabled =
                            state.dist_measured == 1 ? false : true;
                          state.galaxy_vel =
                            Math.floor(Math.random() * 60000) + 5000;
                        "
                      >
                        calculate
                      </v-btn>
                    </v-card-text>
                  </v-card>
                </div>
                <v-card
                  outlined
                  class="pa-5 mt-8"
                  color="orange lighten-5"
                  elevation="0"
                >
                  Watch this video for instructions on measuring wavelengths and
                  velocities based on emission and absorption lines.

                  <div class="text-center mt-4">
                    <video-dialog
                      button-text="learn more"
                      title-text="How do we measure galaxy velocity?"
                      close-text="close"
                      @close="console.log('Close button was clicked.')"
                    >
                      Verbiage about comparing observed and rest wavelengths of
                      absorption/emission lines
                    </video-dialog>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </span>
</template>