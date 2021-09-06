<template>
  <v-app id="cosmicds-app">
    <!-- Tool bar, fixed to the top of the application -->
    <v-app-bar
      color="primary"
      dark
      src="https://cdn.eso.org/images/screen/eso1738b.jpg"
      scroll-target="#scrolling-techniques-4"
    >
      <template v-slot:img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title> Cosmic Data Stories | Hubble's Law </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- The main section of the application -->
    <v-main id="scrolling-techniques-4" class="overflow-y-auto fill-height">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" xl="8">
            <v-card class="d-flex flex-column">
              <!-- This sets up the multi-step sections across the top -->
              <!-- v-model is a 2-way token that controls the state of something in the app -->
              <v-stepper v-model="state.over_model" class="elevation-0">
                <v-stepper-header>
                  <!-- :complete="state.over_model > 1"   
                        : is a binding - binds state of "complete" to the thing in the "".  If over_model is > 1, then we have gone past step 1.
                  therefore, consider step 1 complete. -->
                  <!-- Another example could be something like :disabled = "state.continue_button_disabled==1" -->
                  <v-stepper-step
                    :complete="state.over_model > 1"
                    step="1"
                    editable
                  >
                    Collect Galaxy Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 2"
                    step="2"
                    editable
                  >
                    Estimate Age of Universe
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 3"
                    step="3"
                    editable
                    >Explore Class Data
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                    :complete="state.over_model > 4"
                    step="4"
                    editable
                    >View Distributions
                  </v-stepper-step>
                </v-stepper-header>

                <!-- This sets up the screen for the galaxy selection/measurement step -->
                <v-stepper-items class="no-transition">
                  <!-- This sets up the screen for the Analysis/data fitting step -->

                  <!-- Will need buttons/functionality for:
                     * drawing by eye/calculating/plotting best fit lines
                     * Choosing different data sets - student/class/all
                     * Plotting by galaxy type -->
                  <v-stepper-content step="1">
                    <c-galaxy-analysis />
                  </v-stepper-content>

                  <v-stepper-content step="2">
                    <v-container>
                      <v-row>
                        <v-col cols="3" class="align-stretch">
                          <div class="d-flex mb-4">
                            <v-btn
                              :outlined="state.draw_on"
                              color="orange"
                              class="flex-grow-1 white--text"
                              @click="state.draw_on = !state.draw_on"
                            >
                              draw a fit line
                              <v-spacer></v-spacer>
                              <v-icon right dark class="px-4">
                                mdi-draw
                              </v-icon>
                            </v-btn>
                          </div>
                          <div class="d-flex mb-4">
                            <v-btn
                              color="green lighten-1"
                              class="flex-grow-1 white--text"
                              @click="
                                fit_lines({
                                  viewer_id: 'hub_fit_viewer',
                                });
                                state.bestfit_on = 1;
                              "
                            >
                              generate best fit
                              <v-spacer></v-spacer>
                              <v-icon right dark class="px-4">
                                mdi-calculator
                              </v-icon>
                            </v-btn>
                          </div>
                        </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_fit_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Enable a button to draw your own fit line (unless
                            this is prohibitively complicated). Plot drawn and
                            calculated best fit lines. Display should include
                            only this student's 4-5 data points.
                          </todo-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-card class="pa-8 mx-auto">
                          Watch this video for an explanation how and why we can
                          calculate the age of universe by inverting our
                          <em>H</em><sub>0</sub> value.
                          <div class="text-center mt-4">
                            <video-dialog
                              button-text="learn more"
                              title-text="How do we estimate age of the universe?"
                              close-text="close"
                              @close="console.log('Close button was clicked.')"
                            >
                              Verbiage about how the slope of the Hubble plot is
                              the inverse of the age of the universe.
                            </video-dialog>
                          </div>
                        </v-card>
                      </v-row>
                    </v-container>
                    <!-- Disabling for now
                    <v-btn color="primary" @click="state.over_model = 3">
                      Continue
                    </v-btn>
                    <v-btn text> Cancel </v-btn>
-->
                  </v-stepper-content>

                  <!-- This sets up the screen for the View Results step where they can look at distributions -->
                  <!-- Will need buttons/functionality for choosing different data sets -->
                  <!-- Need to think through whether the hubble plot should also appear on this page or if that would be confusing -->

                  <v-stepper-content step="3">
                    <v-container>
                      <v-row>
                        <v-col cols="3"> </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_const_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Give options to view all data from class, fit a
                            line, and calculate <em>H</em><sub>0</sub> and age
                            values for full class data set.
                          </todo-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-card class="pa-8" elevation="3" width="100%">
                          Buttons to calculate age of universe from H0 value.<br />

                          <help-dialog
                            button-text="Click Me!"
                            title-text="Testing!"
                            accept-text="Okay"
                            cancel-text="Cancel"
                            @accept="console.log('Button was clicked.')"
                          >
                            This is a test of a pure Vue dialog with a custom
                            event.
                          </help-dialog>
                        </v-card>
                      </v-row>
                    </v-container>
                  </v-stepper-content>

                  <v-stepper-content step="4">
                    <v-container>
                      <v-row>
                        <v-col cols="3"> </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              :widget="viewers.hub_const_viewer"
                            ></jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Give options to look at galaxies &amp; distribution
                            of age values for individual students within class
                            or for unique classes within full data set.
                          </todo-alert>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-container>
                      <v-row>
                        <v-col cols="3"> </v-col>
                        <v-col>
                          <v-lazy>
                            <jupyter-widget
                              style="height: 300px"
                              :widget="viewers.age_distr_viewer"
                            >
                            </jupyter-widget>
                          </v-lazy>
                          <todo-alert>
                            Regular histogram to start. Give option to turn into
                            stacked histogram with legend that provide option to
                            select specific students or classes and highlight in
                            top plot galaxies used to get that age estimate.
                          </todo-alert>
                        </v-col>
                      </v-row>
                    </v-container>
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>
                    <v-card
                      class="fill-height mb-12"
                      color="grey lighten-1 elevation-0"
                    ></v-card>
                    <!-- disabling this because it's redundant with previous/next
                    <v-btn color="primary" @click="state.over_model = 1">
                      Continue
                    </v-btn>
                    <v-btn text> Cancel </v-btn>
-->
                    <!-- Curly braces indicate text to be replaced by content in the variable,
                  like {{state.dialog_text}}  (For example, in app.py file, you can collect
                  student userID and display it here via something like "Hello <student userID>".) -->
                  </v-stepper-content>
                </v-stepper-items>
              </v-stepper>
              <v-spacer></v-spacer>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn
                  :disabled="state.over_model == 1 ? true : false"
                  color="primary"
                  @click="
                    state.over_model =
                      state.over_model > 1
                        ? state.over_model - 1
                        : state.over_model
                  "
                >
                  Previous
                </v-btn>
                <v-spacer></v-spacer>

                <!-- for TESTING, use the following -- :disabled="false" -->
                <!-- for FINAL, use the following -- :disabled="state.over_model == 4 ? true : state.next1_disabled" -->
                <v-btn
                  :disabled="false"
                  color="primary"
                  dark
                  @click="
                    state.over_model =
                      state.over_model < 4
                        ? state.over_model + 1
                        : state.over_model
                  "
                >
                  {{ state.over_model == 4 ? "Finish" : "Next" }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <c-footer />
      </v-container>
    </v-main>

    <v-snackbar
      v-model="state.gal_snackbar"
      style="position: absolute"
      color="green"
    >
      Galaxy selected.
      <v-btn dark text @click="state.gal_snackbar = 0"> Close </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.dist_snackbar"
      style="position: absolute"
      color="green"
    >
      Distance measured.
      <v-btn
        dark
        text
        @click="
          state.dist_snackbar = 0;
          state.col_tab_model = 1;
        "
      >
        Go to Measure Velocity
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.marker_snackbar"
      style="position: absolute"
      color="green"
    >
      Wavelength marker set.
      <v-btn dark text @click="state.marker_snackbar = 0"> Close </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.vel_snackbar"
      style="position: absolute"
      color="green"
    >
      Velocity measured.
      <v-btn
        dark
        text
        @click="
          state.vel_snackbar = 0;
          state.col_tab_model = 0;
        "
      >
        Go to Estimate Distance
      </v-btn>
    </v-snackbar>

    <v-snackbar
      v-model="state.data_ready_snackbar"
      style="position: absolute"
      color="primary"
    >
      Great! You've estimated both distance and velocity for your galaxy. Now
      you can add these measurements to your dataset.
      <v-btn text @click="state.data_ready_snackbar = 0" icon large dark>
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-snackbar>
  </v-app>
</template>

<style id="cosmicds-app">
html {
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
.jupyter-widgets .jp-Cell .jp-CodeCell .jp-Notebook-cell .jp-mod-noInput {
  margin: 0;
  padding: 0;
}
#cosmicds-app {
  height: 100%;
}
#app {
  height: 100vh;
}
.card-outter {
  position: relative;
  padding-bottom: 50px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
.v-stepper__wrapper {
  height: 100%;
}
.bqplot {
  height: 100%;
}
.v-stepper__content {
  min-height: 500px;
}
.v-tabs-items {
  min-height: 300px;
}

.no-transition .v-stepper__content {
  transition: none !important;
}
</style>
