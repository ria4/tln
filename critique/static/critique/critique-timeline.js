///////////////////////
// Timeline creation //
///////////////////////

// DOM element where the Timeline will be attached
const timelineContainer = document.getElementById("timeline");
const timelineFiltersContainer = document.getElementById("timeline-filters");

// Create the initial items
const timelineItems = new vis.DataSet(timelineItemsRaw);

// Create the groups
const timelineGroups = new vis.DataSet(timelineGroupsRaw);

// Configuration for the Timeline
const now = new Date();
const timelineMinDate = new Date(2022, 3, 25);
let timelineEndDate = new Date(timelineMinDate.getTime());
timelineEndDate.setMonth(timelineMinDate.getMonth() + 4);
const timelineMaxDate = new Date(now.getFullYear(), now.getMonth(), now.getDay() + 10);
const timelineOptions = {
  // disable XSS protection, since there is no user input
  // and we need items not to be stripped of their html attributes
  xss: {
    disabled: true,
  },
  // set a fixed height covering the maximum number of visible items
  // and then add the height of the tooltip (because we can't use both
  // overflow-x: hidden and overflow-y: visible, because CSS is shit)
  height: "644px",
  // options related to items
  selectable: false,
  margin: {
    item: 5,
  },
  // options related to dates
  min: timelineMinDate,
  start: timelineMinDate,
  end: timelineEndDate,
  max: timelineMaxDate,
  format: {
    minorLabels: {
      weekday: "dddd D",
      month: "MMMM",
    }
  },
  locale: "fr_FR",
  showCurrentTime: false,
  // display dates in UTC rather than local timezone
  moment: function(date) { return vis.moment(date).utcOffset('+00:00'); },
  // options related to scroll and zoom
  horizontalScroll: true,
  zoomKey: "ctrlKey",
  zoomMin: 1000*60*60*24*5,
};

// Create a Timeline
const timeline = new vis.Timeline(
  timelineContainer,
  timelineItems,
  timelineGroups,
  timelineOptions,
);

// Remove user help on mobile
if (isTouchDevice()) {
  let timelineHelp = document.querySelector("#timeline .vis-panel.vis-background.vis-horizontal");
  timelineHelp.style.setProperty('--after-display', "none");
}

/////////////
// Filters //
/////////////

const timelineFilterButtons = document.querySelectorAll("#timeline-filters span");
let isGroupFilter = null;
let filterValue = null;

function applyFilter(isGroupFilter, filterValue) {
  if (filterValue === null) { return }
  let querySelectorValid =
    isGroupFilter
    ? ".vis-group-" + filterValue + " .vis-item"
    : ".vis-item-tag-" + filterValue;
  let querySelectorInvalid =
    isGroupFilter
    ? ".vis-group:not(.vis-group-" + filterValue + ") .vis-item"
    : ".vis-item:not(.vis-item-tag-" + filterValue + ")";
  timelineContainer.querySelectorAll(querySelectorValid).forEach(
    (el) => el.classList.remove("transparent")
  );
  timelineContainer.querySelectorAll(querySelectorInvalid).forEach(
    (el) => el.classList.add("transparent")
  );
}

function toggleFilter(filterButton) {
  if (!filterButton.classList.contains("active")) {
    isGroupFilter = filterButton.hasAttribute("data-filter-group");
    filterValue = filterButton.getAttribute("data-filter");
    applyFilter(isGroupFilter, filterValue);
    timelineFilterButtons.forEach((el) => el.classList.remove("active"));
    filterButton.classList.add("active");
  } else {
    isGroupFilter = null;
    filterValue = null;
    let visItems = timelineContainer.querySelectorAll(".vis-item");
    visItems.forEach((item) => item.classList.remove("transparent"));
    timelineFilterButtons.forEach((el) => el.classList.remove("active"));
  }
}


///////////////
// Callbacks //
///////////////

// Declare global variables used in "changed" and "itemover" callbacks
let windowMinTime;
let windowMinTimeExtended;
let windowMaxTime;
let windowMaxTimeExtended;
let windowSpanTime;

// Setup variables for timeline initial animation
let firstTimelineDraw = true;
let firstTimelineDrawComplete = false;
const visPanelCenter = document.querySelector(".vis-panel.vis-center");
visPanelCenter.classList.add("furthest-right");

// Callback for "changed" event
timeline.on("changed", function(properties) {
  // small hack to detect full drawing of the timeline
  // (the provided onInitialDrawComplete does not work)
  // we also have to wait for 1+ second, because the 'changed' event
  // and the actual showing of the timeline do not match exactly...
  if (firstTimelineDraw) {
    setTimeout(function() {
      // switch from transparent to opaque
      timelineContainer.classList.remove("transparent");
      timelineFiltersContainer.classList.remove("transparent");
      // center to 2 months before the maximum date,
      // this should stick the maximum date to the right of the timeline
      const timelineStartDate = new Date(timelineMaxDate.getTime());
      timelineStartDate.setMonth(timelineMaxDate.getMonth() - 2);
      timeline.moveTo(timelineStartDate, () => firstTimelineDrawComplete = true);
    }, 1200);
    firstTimelineDraw = false;
  }

  // after the initial moveTo animation,
  if (!firstTimelineDrawComplete) { return }

  // hide side shadows when the timeline gets close to its min/max dates
  let timelineWindow = timeline.getWindow();
  windowMinTime = timelineWindow.start.getTime();
  windowMaxTime = timelineWindow.end.getTime();
  windowSpanTime = windowMaxTime - windowMinTime;
  windowMinTimeExtended = windowMinTime - .04 * windowSpanTime;
  windowMaxTimeExtended = windowMaxTime + .04 * windowSpanTime;
  if (timelineWindow.start.getTime() - timelineMinDate.getTime() <= .05 * windowSpanTime) {
    visPanelCenter.classList.add("furthest-left");
  } else {
    visPanelCenter.classList.remove("furthest-left");
  }
  if (timelineMaxDate.getTime() - timelineWindow.end.getTime() <= .05 * windowSpanTime) {
    visPanelCenter.classList.add("furthest-right");
  } else {
    visPanelCenter.classList.remove("furthest-right");
  }

  // apply optional filter
  applyFilter(isGroupFilter, filterValue);

  // reset the overflowing status of items
  (document.querySelectorAll(".vis-item-overflowing")).forEach(
    (el) => {
      let elDetails = el.querySelector(".vis-item-details");
      elDetails.style.removeProperty("left");
      el.classList.remove("vis-item-overflowing");
    }
  );
  (document.querySelectorAll(".vis-item-not-overflowing")).forEach(
    (el) => el.classList.remove("vis-item-not-overflowing")
  );
});

// Callback for "itemover" event
let itemZIndex = 1;
timeline.on("itemover", function(properties) {
  let visItem = document.getElementsByClassName("vis-item-" + properties.item)[0];

  // lazy-load images
  let visItemDetails = visItem.querySelector(".vis-item-details");
  let visItemImg = visItemDetails.querySelector("img");
  if (visItemImg.hasAttribute("data-src")) {
      visItemImg.setAttribute("src", visItemImg.getAttribute("data-src"));
      visItemImg.removeAttribute("data-src");
  }

  // reposition the tooltip if the item is overflowing
  // (check first if it was already processed)
  if (
    !visItem.classList.contains("vis-item-overflowing")
    && !visItem.classList.contains("vis-item-not-overflowing")
  ) {
    let timelineItem = timelineItems.get(properties.item);
    let timelineItemStartTime = timelineItem.start.getTime();
    let timelineItemEndTime = timelineItem.end.getTime();
    if (
      timelineItemStartTime > windowMinTimeExtended
      && timelineItemEndTime < windowMaxTimeExtended
    ) {
      visItem.classList.add("vis-item-not-overflowing");
    } else {
      visItem.classList.add("vis-item-overflowing");
      let visItemVisibleSpanTime = (
        Math.min(timelineItemEndTime, windowMaxTime)
        - Math.max(timelineItemStartTime, windowMinTime)
      );
      let x = visItemVisibleSpanTime * visPanelCenter.offsetWidth / windowSpanTime / 2 * .96;
      visItemDetails.style.left = Math.floor(x) + "px";
    }
  }

  // put the most recently hovered item (and its details) on top of other items
  setTimeout(function() {
    // enact the change only if the user isn't hovering on a tooltip after 0.1 second
    if (!document.querySelector(".vis-item-details:hover")) {
      // that's a cool hack
      visItem.style.zIndex = ++itemZIndex;
    }
  }, 100);
})

// Callback for "mouseUp" event
timeline.on("mouseUp", function(properties) {
  // center the timeline on an item when clicked
  if (properties.what == "item") {
    timeline.focus(properties.item);
  }
})
