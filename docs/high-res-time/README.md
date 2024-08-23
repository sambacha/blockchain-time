---
created: 2024-08-12T16:37:58 (UTC -07:00)
tags: []
source: https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time
author: Yoav Weiss (Google LLC)
---

# High Resolution Time

> ## Excerpt
> This specification defines an API that provides the time origin, and
        current time in sub-millisecond resolution, such that it is not subject
        to system clock skew or adjustments.

---
## Abstract

This specification defines an API that provides the time origin, and current time in sub-millisecond resolution, such that it is not subject to system clock skew or adjustments.

## Status of This Document

_This section describes the status of this document at the time of its publication. A list of current W3C publications and the latest revision of this technical report can be found in the [W3C technical reports index](https://www.w3.org/TR/) at https://www.w3.org/TR/._

This document was published by the [Web Performance Working Group](https://www.w3.org/groups/wg/webperf) as an Editor's Draft.

Publication as an Editor's Draft does not imply endorsement by W3C and its Members.

This is a draft document and may be updated, replaced or obsoleted by other documents at any time. It is inappropriate to cite this document as other than work in progress.

This document was produced by a group operating under the [W3C Patent Policy](https://www.w3.org/policies/patent-policy/). W3C maintains a [public list of any patent disclosures](https://www.w3.org/groups/wg/webperf/ipr) made in connection with the deliverables of the group; that page also includes instructions for disclosing a patent. An individual who has actual knowledge of a patent which the individual believes contains [Essential Claim(s)](https://www.w3.org/policies/patent-policy/#def-essential) must disclose the information in accordance with [section 6 of the W3C Patent Policy](https://www.w3.org/policies/patent-policy/#sec-Disclosure).

This document is governed by the [03 November 2023 W3C Process Document](https://www.w3.org/policies/process/20231103/).

## Table of Contents

1.  [Abstract](https://w3c.github.io/hr-time/#abstract)
2.  [Status of This Document](https://w3c.github.io/hr-time/#sotd)
3.  [1. Introduction](https://w3c.github.io/hr-time/#introduction)
    1.  [1.1 Use-cases](https://w3c.github.io/hr-time/#use-cases)
    2.  [1.2 Examples](https://w3c.github.io/hr-time/#examples)
4.  [2. Time Concepts](https://w3c.github.io/hr-time/#sec-concepts)
    1.  [2.1 Clocks](https://w3c.github.io/hr-time/#sec-clocks)
    2.  [2.2 Moments and Durations](https://w3c.github.io/hr-time/#moments-and-durations)
5.  [3. Tools for Specification Authors](https://w3c.github.io/hr-time/#sec-tools)
    1.  [3.1 Examples](https://w3c.github.io/hr-time/#sec-tools-examples)
6.  [4. Time Origin](https://w3c.github.io/hr-time/#sec-time-origin)
7.  [5. The `DOMHighResTimeStamp` typedef](https://w3c.github.io/hr-time/#sec-domhighrestimestamp)
8.  [6. The `EpochTimeStamp` typedef](https://w3c.github.io/hr-time/#the-epochtimestamp-typedef)
9.  [7. The `Performance` interface](https://w3c.github.io/hr-time/#sec-performance)
    1.  [7.1 `now()` method](https://w3c.github.io/hr-time/#now-method)
    2.  [7.2 `timeOrigin` attribute](https://w3c.github.io/hr-time/#timeorigin-attribute)
    3.  [7.3 `toJSON()` method](https://w3c.github.io/hr-time/#tojson-method)
10.  [8. Extensions to `WindowOrWorkerGlobalScope` mixin](https://w3c.github.io/hr-time/#extensions-to-windoworworkerglobalscope-mixin)
    1.  [8.1 The `performance` attribute](https://w3c.github.io/hr-time/#the-performance-attribute)
11.  [9. Security Considerations](https://w3c.github.io/hr-time/#sec-security)
    1.  [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution)
    2.  [9.2 Clock drift](https://w3c.github.io/hr-time/#clock-drift)
12.  [10. Privacy Considerations](https://w3c.github.io/hr-time/#sec-privacy)
13.  [11. Conformance](https://w3c.github.io/hr-time/#conformance)
14.  [A. Index](https://w3c.github.io/hr-time/#index)
    1.  [A.1 Terms defined by this specification](https://w3c.github.io/hr-time/#index-defined-here)
    2.  [A.2 Terms defined by reference](https://w3c.github.io/hr-time/#index-defined-elsewhere)
15.  [B. IDL Index](https://w3c.github.io/hr-time/#idl-index)
16.  [C. Acknowledgments](https://w3c.github.io/hr-time/#acknowledgments)
17.  [D. References](https://w3c.github.io/hr-time/#references)
    1.  [D.1 Normative references](https://w3c.github.io/hr-time/#normative-references)
    2.  [D.2 Informative references](https://w3c.github.io/hr-time/#informative-references)

_This section is non-normative._

The ECMAScript Language specification \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] defines the `[Date](https://tc39.es/ecma262/multipage/#sec-date-objects)` object as a time value representing time in milliseconds since 01 January, 1970 UTC. For most purposes, this definition of time is sufficient as these values represent time to millisecond precision for any moment that is within approximately 285,616 years from 01 January, 1970 UTC.

In practice, these definitions of time are subject to both clock skew and adjustment of the system clock. The value of time may not always be monotonically increasing and subsequent values may either decrease or remain the same.

For example, the following script may record a positive number, negative number, or zero for computed `duration`:

[Example 1](https://w3c.github.io/hr-time/#example-1)

```
<span>var</span> mark_start = <span>Date</span>.now();
doTask(); <span>// Some task</span>
<span>var</span> duration = <span>Date</span>.now() - mark_start;
```

For certain tasks this definition of time may not be sufficient as it:

-   Does not have a stable monotonic clock, and as a result, it is subject to system clock skew.
-   Does not provide sub-millisecond time resolution.

This specification does not propose changing the behavior of `[Date.now()](https://tc39.es/ecma262/multipage/#sec-date.now)` \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] as it is genuinely useful in determining the current value of the calendar time and has a long history of usage. The [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type, [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method, and [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attributes of the [`Performance`](https://w3c.github.io/hr-time/#dom-performance) interface resolve the above issues by providing monotonically increasing time values with sub-millisecond resolution.

Note

Providing sub-millisecond resolution is not a mandatory part of this specification. Implementations may choose to limit the timer resolution they expose for privacy and security reasons, and not expose sub-millisecond timers. Use-cases that rely on sub-millisecond resolution may not be satisfied when that happens.

_This section is non-normative._

This specification defines a few different capabilities: it provides timestamps based on a stable, monotonic clock, comparable across contexts, with potential sub-millisecond resolution.

The need for a stable monotonic clock when talking about performance measurements stems from the fact that unrelated clock skew can distort measurements and render them useless. For example, when attempting to accurately measure the elapsed time of navigating to a Document, fetching of resources or execution of script, a monotonically increasing clock with sub-millisecond resolution is desired.

Comparing timestamps between contexts is essential e.g. when synchronizing work between a [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker) and the main thread or when instrumenting such work in order to create a unified view of the event timeline.

Finally, the need for sub-millisecond timers revolves around the following use-cases:

-   Ability to schedule work in sub-millisecond intervals. That is particularly important on the main thread, where work can interfere with frame rendering which needs to happen in short and regular intervals, to avoid user-visible jank.
-   When calculating the frame rate of a script-based animation, developers will need sub-millisecond resolution in order to determine if an animation is drawing at 60 FPS. Without sub-millisecond resolution, a developer can only determine if an animation is drawing at 58.8 FPS (1000ms / 16) or 62.5 FPS (1000ms / 17).
-   When collecting in-the-wild measurements of JS code (e.g. using User-Timing), developers may be interested in gathering sub-milliseconds timing of their functions, to catch regressions early.
-   When attempting to cue audio to a specific point in an animation or ensure that the audio and animation are perfectly synchronized, developers will need to accurately measure the amount of time elapsed.

_This section is non-normative._

A developer may wish to construct a timeline of their entire application, including events from [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker) or [`SharedWorker`](https://html.spec.whatwg.org/multipage/workers.html#sharedworker), which have different [time origins](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin). To display such events on the same timeline, the application can translate the [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)s with the help of the [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute.

[Example 2](https://w3c.github.io/hr-time/#example-2)

```
<span>// ---- worker.js -----------------------------</span>
<span>// Shared worker script</span>
onconnect = <span><span>function</span>(<span>e</span>) </span>{
  <span>var</span> port = e.ports[<span>0</span>];
  port.onmessage = <span><span>function</span>(<span>e</span>) </span>{
    <span>// Time execution in worker</span>
    <span>var</span> task_start = performance.now();
    result = runSomeWorkerTask();
    <span>var</span> task_end = performance.now();
  }

  <span>// Send results and epoch-relative timestamps to another context</span>
  port.postMessage({
    <span>'task'</span>: <span>'Some worker task'</span>,
    <span>'start_time'</span>: task_start + performance.timeOrigin,
    <span>'end_time'</span>: task_end + performance.timeOrigin,
    <span>'result'</span>: result
  });
}

<span>// ---- application.js ------------------------</span>
<span>// Timing tasks in the document</span>
<span>var</span> task_start = performance.now();
runSomeApplicationTask();
<span>var</span> task_end = performance.now();

<span>// developer provided method to upload runtime performance data</span>
reportEventToAnalytics({
  <span>'task'</span>: <span>'Some document task'</span>,
  <span>'start_time'</span>: task_start,
  <span>'duration'</span>: task_end - task_start
});

<span>// Translating worker timestamps into document's time origin</span>
<span>var</span> worker = <span>new</span> SharedWorker(<span>'worker.js'</span>);
worker.port.onmessage = <span><span>function</span> (<span>event</span>) </span>{
  <span>var</span> msg = event.data;

  <span>// translate epoch-relative timestamps into document's time origin</span>
  msg.start_time = msg.start_time - performance.timeOrigin;
  msg.end_time = msg.end_time - performance.timeOrigin;

  reportEventToAnalytics(msg);
}
```

A clock tracks the passage of time and can report the unsafe current time that an algorithm step is executing. There are many kinds of clocks. All clocks on the web platform attempt to count 1 millisecond of clock time per 1 millisecond of real-world time, but they differ in how they handle cases where they can't be exactly correct.

-   The wall clock's unsafe current time is always as close as possible to a user's notion of time. Since a computer sometimes runs slow or fast or loses track of time, its [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) sometimes needs to be adjusted, which means the [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time) can decrease, making it unreliable for performance measurement or recording the orders of events. The web platform shares a [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) with \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range).
-   The monotonic clock's unsafe current time never decreases, so it can't be changed by system clock adjustments. The [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) only exists within a single execution of the [user agent](https://infra.spec.whatwg.org/#user-agent), so it can't be used to compare events that might happen in different executions.
    
    Note
    
    Since the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) can't be adjusted to match the user's notion of time, it should be used for measurement, rather than user-visible times. For any time communication with the user, use the wall clock.
    
    Note
    
    The user agent can pick a new [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) when the browser restarts, when it starts an isolated browsing session—e.g. incognito or a similar browsing mode—or when it creates an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) that can't communicate with any existing settings objects. As a result, developers should not use shared timestamps as absolute time that holds its monotonic properties across all past, present, and future contexts; in practice, the monotonic properties only apply for contexts that can reach each other by exchanging messages via one of the provided messaging mechanisms - e.g. [`postMessage`](https://html.spec.whatwg.org/multipage/web-messaging.html#dom-window-postmessage-options)`(message, options)`, [`BroadcastChannel`](https://html.spec.whatwg.org/multipage/web-messaging.html#broadcastchannel), etc.
    
    Note
    
    In certain scenarios (e.g. when a tab is backgrounded), the user agent may choose to throttle timers and periodic callbacks run in that context or even freeze them entirely. Any such throttling should not affect the resolution or accuracy of the time returned by the monotonic clock.
    

Each [clock](https://w3c.github.io/hr-time/#dfn-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#dfn-unsafe-current-time) returns an unsafe moment. [Coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) converts these [unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) to coarsened moments or just [moments](https://w3c.github.io/hr-time/#dfn-moment). [Unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) and [moments](https://w3c.github.io/hr-time/#dfn-moment) from different clocks are not comparable.

Note

[Moments](https://w3c.github.io/hr-time/#dfn-moment) and [unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) represent points in time, which means they can't be directly stored as numbers. Implementations will usually represent a [moment](https://w3c.github.io/hr-time/#dfn-moment) as a [duration](https://w3c.github.io/hr-time/#dfn-duration) from some other fixed point in time, but specifications ought to deal in the [moments](https://w3c.github.io/hr-time/#dfn-moment) themselves.

A duration is the distance from one [moment](https://w3c.github.io/hr-time/#dfn-moment) to another from the same [clock](https://w3c.github.io/hr-time/#dfn-clock). Neither endpoint can be an [unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment) so that both [durations](https://w3c.github.io/hr-time/#dfn-duration) and differences of [durations](https://w3c.github.io/hr-time/#dfn-duration) mitigate the concerns in [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution). [Durations](https://w3c.github.io/hr-time/#dfn-duration) are measured in milliseconds, seconds, etc. Since all [clocks](https://w3c.github.io/hr-time/#dfn-clock) attempt to count at the same rate, [durations](https://w3c.github.io/hr-time/#dfn-duration) don't have an associated [clock](https://w3c.github.io/hr-time/#dfn-clock), and a [duration](https://w3c.github.io/hr-time/#dfn-duration) calculated from two [moments](https://w3c.github.io/hr-time/#dfn-moment) on one clock can be added to a [moment](https://w3c.github.io/hr-time/#dfn-moment) from a second [clock](https://w3c.github.io/hr-time/#dfn-clock), to produce another [moment](https://w3c.github.io/hr-time/#dfn-moment) on that second [clock](https://w3c.github.io/hr-time/#dfn-clock).

The duration from a to b is the result of the following algorithm:

1.  [Assert](https://infra.spec.whatwg.org/#assert): a was created by the same [clock](https://w3c.github.io/hr-time/#dfn-clock) as b.
2.  [Assert](https://infra.spec.whatwg.org/#assert): Both a and b are [coarsened moments](https://w3c.github.io/hr-time/#dfn-moment).
3.  Return the amount of time from a to b as a [duration](https://w3c.github.io/hr-time/#dfn-duration). If b came before a, this will be a negative [duration](https://w3c.github.io/hr-time/#dfn-duration).

[Durations](https://w3c.github.io/hr-time/#dfn-duration) can be used implicitly as [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)s. To implicitly convert a duration to a timestamp, given a [duration](https://w3c.github.io/hr-time/#dfn-duration) d, return the number of milliseconds in d.

For measuring time within a single page (within the context of a single [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)), use the settingsObject's current relative timestamp, defined as the [duration from](https://w3c.github.io/hr-time/#dfn-duration-from) settingsObject's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) to the settingsObject's [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time). This value can be exposed directly to JavaScript using the [duration](https://w3c.github.io/hr-time/#dfn-duration)'s [implicit conversion](https://w3c.github.io/hr-time/#dfn-implicitly-convert-a-duration-to-a-timestamp) to [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp).

For measuring time within a single UA execution when an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) isn't an appropriate base for comparison, create [moments](https://w3c.github.io/hr-time/#dfn-moment) using an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time). An [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) settingsObject's current monotonic time is the result of the following steps:

1.  Let unsafeMonotonicTime be the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time).
2.  Return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with unsafeMonotonicTime and settingsObject's [cross-origin isolated capability](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability).

[Moments](https://w3c.github.io/hr-time/#dfn-moment) from the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) can't be directly represented in JavaScript or HTTP. Instead, expose a [duration](https://w3c.github.io/hr-time/#dfn-duration) between two such [moments](https://w3c.github.io/hr-time/#dfn-moment).

For measuring time across multiple UA executions, create [moments](https://w3c.github.io/hr-time/#dfn-moment) using the [current wall time](https://w3c.github.io/hr-time/#dfn-current-wall-time) or (if you need higher precision in [cross-origin-isolated contexts](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability)) an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time). The current wall time is the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).

An [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) settingsObject's current wall time is the result of the following steps:

1.  Let unsafeWallTime be the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).
2.  Return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with unsafeWallTime and settingsObject's [cross-origin isolated capability](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability).

When using [moments](https://w3c.github.io/hr-time/#dfn-moment) from the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock), be sure that your design accounts for situations when the user adjusts their clock either forward or backward.

[Moments](https://w3c.github.io/hr-time/#dfn-moment) from the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) can be represented in JavaScript by passing the number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to that [moment](https://w3c.github.io/hr-time/#dfn-moment) into the [`` `Date` ``](https://tc39.es/ecma262/multipage/#sec-date-objects) constructor, or by passing the number of nanoseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to that [moment](https://w3c.github.io/hr-time/#dfn-moment) into the [Temporal.Instant](https://tc39.es/proposal-temporal/#sec-temporal-instant-constructor) constructor.

Avoid sending similar representations between computers, as doing so will expose the user's clock skew, which is a [tracking vector](https://infra.spec.whatwg.org/#tracking-vector). Instead, use an approach similar to [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) [moments](https://w3c.github.io/hr-time/#dfn-moment) of sending a duration between two [moments](https://w3c.github.io/hr-time/#dfn-moment).

The age of an error report can be computed using:

7.  Initialize report's [generation time](https://www.w3.org/TR/reporting-1/#report-timestamp) to settings' [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time).

Later:

2.  Let data be a map with the following key/value pairs:
    
    age
    
    The number of milliseconds between report's [generation time](https://www.w3.org/TR/reporting-1/#report-timestamp) and context's [relevant settings object](https://html.spec.whatwg.org/multipage/webappapis.html#relevant-settings-object)'s [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time), rounded to the nearest integer.
    
    ...
    

Multi-day attribution report expirations can be handled as:

2.  Let source be a new attribution source struct whose items are:
    
    ...
    
    source time
    
    context's [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time)
    
    expiry
    
    [parse a duration string](https://html.spec.whatwg.org/multipage/#parse-a-duration-string) from `value["expiry"]`
    

Days later:

2.  If context's [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time) is less than source's source time + source's expiry, send a report.

The Unix epoch is the [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) corresponding to 1 January 1970 00:00:00 UTC.

Each group of [environment settings objects](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) that could possibly communicate in any way has an estimated monotonic time of the Unix epoch, a [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock), whose value is initialized by the following steps:

1.  Let wall time be the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).
2.  Let monotonic time be the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time).
3.  Let epoch time be `monotonic time - (wall time - [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch))`
4.  Initialize the [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) to the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with epoch time.

Issue 1

The above set of settings-objects-that-could-possibly-communicate needs to be specified better. It's similar to [familiar with](https://html.spec.whatwg.org/multipage/browsers.html#familiar-with) but includes [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker)

s.

Performance measurements report a [duration](https://w3c.github.io/hr-time/#dfn-duration) from a [moment](https://w3c.github.io/hr-time/#dfn-moment) early in the initialization of a relevant [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object). That [moment](https://w3c.github.io/hr-time/#dfn-moment) is stored in that settings object's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).

To get time origin timestamp, given a [global object](https://html.spec.whatwg.org/multipage/webappapis.html#global-object) global, run the following steps, which return a [duration](https://w3c.github.io/hr-time/#dfn-duration):

1.  Let timeOrigin be global's [relevant settings object](https://html.spec.whatwg.org/multipage/webappapis.html#relevant-settings-object)'s [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).
    
2.  Return the [duration from](https://w3c.github.io/hr-time/#dfn-duration-from) the [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) to timeOrigin.

Note

The value returned by [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp) is approximately the time after the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) that global's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) happened. It may differ from the value returned by [`Date.now()`](https://tc39.es/ecma262/multipage/#sec-date.now) executed at the time origin, because the former is recorded with respect to a [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) that is not subject to system and user clock adjustments, clock skew, and so on.

The coarsen time algorithm, given an

[unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment)

timestamp on some

[clock](https://w3c.github.io/hr-time/#dfn-clock)

and an optional boolean crossOriginIsolatedCapability (default false), runs the following steps:

1.  Let time resolution be 100 microseconds, or a higher [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) value.
2.  If crossOriginIsolatedCapability is true, set time resolution to be 5 microseconds, or a higher [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) value.
3.  In an [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) manner, coarsen and potentially jitter timestamp such that its resolution will not exceed time resolution.
4.  Return timestamp as a [moment](https://w3c.github.io/hr-time/#dfn-moment).

The current high resolution time given a [global object](https://html.spec.whatwg.org/multipage/webappapis.html#global-object) current global must return the result of [relative high resolution time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-time) given [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time) and current global.

The coarsened shared current time given an optional boolean crossOriginIsolatedCapability (default false), must return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with the [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time) and crossOriginIsolatedCapability.

The unsafe shared current time must return the [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time) of the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock).

The [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type is used to store a [duration](https://w3c.github.io/hr-time/#dfn-duration) in milliseconds. Depending on its context, it may represent the [moment](https://w3c.github.io/hr-time/#dfn-moment) that is this [duration](https://w3c.github.io/hr-time/#dfn-duration) after a base [moment](https://w3c.github.io/hr-time/#dfn-moment) like a [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) or the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch).

```
<span data-idl="" id="idl-def-domhighrestimestamp" data-title="DOMHighResTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-double" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-double" id="ref-for-index-term-double-type-1">double<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-6"><code>DOMHighResTimeStamp<!---0.544438%--></code></a>;<!---0.544438%--></span><!---0.544438%-->
```

A [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) _SHOULD_ represent a time in milliseconds accurate enough to allow measurement while preventing timing attacks - see [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution) for additional considerations.

Note

A [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) is a [`double`](https://webidl.spec.whatwg.org/#idl-double), so it can only represent an epoch-relative time—the number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to a [moment](https://w3c.github.io/hr-time/#dfn-moment)—to a finite resolution. For [moments](https://w3c.github.io/hr-time/#dfn-moment) in 2023, that resolution is approximately 0.2 microseconds.

```
<span data-idl="" id="idl-def-epochtimestamp" data-title="EpochTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-unsigned-long-long" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-unsigned-long-long" id="ref-for-index-term-unsigned-long-long-type-1">unsigned long long<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-epochtimestamp" id="ref-for-dom-epochtimestamp-1"><code>EpochTimeStamp<!---0.544438%--></code></a>;<!---0.544438%--></span><!---0.544438%-->
```

Note

: Legacy platform feature

A [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp) represents an integral number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to a given [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock), excluding leap seconds. Specifications that use this type define how the number of milliseconds are interpreted.

```
<span data-idl="" id="idl-def-performance" data-title="Performance">[<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Exposed" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Exposed" id="ref-for-index-term-exposed-extended-attribute-1">Exposed<!---0.544438%--></a>=(Window,Worker)<!---0.544438%--></span>]
interface <a data-link-for="" data-link-type="interface" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-5"><code>Performance<!---0.544438%--></code></a> : <span><a data-link-type="idl" data-xref-type="_IDL_" data-cite="dom" data-cite-path="/" data-cite-frag="eventtarget" data-type="interface" href="https://dom.spec.whatwg.org/#eventtarget" id="ref-for-index-term-eventtarget-interface-1">EventTarget<!---0.544438%--></a><!---0.544438%--></span> {<span data-idl="" id="idl-def-performance-now" data-title="now" data-dfn-for="Performance"><span>
    <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-10"><code>DOMHighResTimeStamp<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-now" id="ref-for-dom-performance-now-2"><code>now<!---0.544438%--></code></a>();<!---0.544438%--></span><span data-idl="" id="idl-def-performance-timeorigin" data-title="timeOrigin" data-dfn-for="Performance">
    readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-11"><code>DOMHighResTimeStamp<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-performance-timeorigin" id="ref-for-dom-performance-timeorigin-3"><code>timeOrigin<!---0.544438%--></code></a>;<!---0.544438%--></span><span data-idl="" id="idl-def-performance-tojson" data-title="toJSON" data-dfn-for="Performance">
    [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Default" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Default" id="ref-for-index-term-default-extended-attribute-1">Default<!---0.544438%--></a><!---0.544438%--></span>]<span> <a data-link-type="interface" data-xref-type="interface" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-object" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-object" id="ref-for-index-term-object-type-1">object<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-tojson" id="ref-for-dom-performance-tojson-1"><code>toJSON<!---0.544438%--></code></a>();<!---0.544438%--></span>
};<!---0.544438%--></span><!---0.544438%-->
```

The `now()` method _MUST_ return the number of milliseconds in the [current high resolution time](https://w3c.github.io/hr-time/#dfn-current-high-resolution-time) given [this](https://webidl.spec.whatwg.org/#this)'s [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) (a [duration](https://w3c.github.io/hr-time/#dfn-duration)).

tests: 2

-   [basic](https://wpt.live/hr-time/basic.any.html)
-   [basic](https://wpt.live/hr-time/basic.any.worker.html)

The time values returned when calling the [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method on [`Performance`](https://w3c.github.io/hr-time/#dom-performance) objects with the same [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) _MUST_ use the same [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock). The difference between any two chronologically recorded time values returned from the [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method _MUST_ never be negative if the two time values have the same [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).

tests: 2

-   [monotonic-clock](https://wpt.live/hr-time/monotonic-clock.any.html)
-   [monotonic-clock](https://wpt.live/hr-time/monotonic-clock.any.worker.html)

The `timeOrigin` attribute _MUST_ return the number of milliseconds in the [duration](https://w3c.github.io/hr-time/#dfn-duration) returned by [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp) for the [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) of [this](https://webidl.spec.whatwg.org/#this).

tests: 2

-   [timeOrigin](https://wpt.live/hr-time/timeOrigin.html)
-   [window-worker-timeOrigin](https://wpt.live/hr-time/window-worker-timeOrigin.window.html)

The time values returned when getting [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) _MUST_ use the same [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) that is shared by [time origins](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin), and whose reference point is the \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range) definition - see [9\. Security Considerations](https://w3c.github.io/hr-time/#sec-security).

tests: 1

-   [test\_cross\_frame\_start](https://wpt.live/hr-time/test_cross_frame_start.html)

When `toJSON()` is called, run \[[WEBIDL](https://w3c.github.io/hr-time/#bib-webidl "Web IDL Standard")\]'s [default toJSON steps](https://webidl.spec.whatwg.org/#default-tojson-steps).

tests: 1

-   [performance-tojson](https://wpt.live/hr-time/performance-tojson.html)

The `performance` attribute on the interface mixin [`WindowOrWorkerGlobalScope`](https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope) allows access to performance related attributes and methods from the [global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-realm-global).

```
<span data-idl="" id="idl-def-windoworworkerglobalscope-partial-1" data-title="WindowOrWorkerGlobalScope">partial interface mixin <a data-idl="partial" data-link-type="interface" data-title="WindowOrWorkerGlobalScope" data-xref-type="interface" data-dfn-for="WindowOrWorkerGlobalScope" data-cite="html" data-cite-path="/webappapis.html" data-cite-frag="windoworworkerglobalscope" data-type="interface" href="https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope" id="ref-for-index-term-windoworworkerglobalscope-interface-2">WindowOrWorkerGlobalScope<!---0.544438%--></a> {<span data-idl="" id="idl-def-windoworworkerglobalscope-performance" data-title="performance" data-dfn-for="WindowOrWorkerGlobalScope">
  [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Replaceable" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Replaceable" id="ref-for-index-term-replaceable-extended-attribute-1">Replaceable<!---0.544438%--></a><!---0.544438%--></span>] readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-8"><code>Performance<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="WindowOrWorkerGlobalScope" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance" id="ref-for-dom-windoworworkerglobalscope-performance-1"><code>performance<!---0.544438%--></code></a>;<!---0.544438%--></span>
};<!---0.544438%--></span><!---0.544438%-->
```

Access to accurate timing information, both for measurement and scheduling purposes, is a common requirement for many applications. For example, coordinating animations, sound, and other activity on the page requires access to high-resolution time to provide a good user experience. Similarly, measurement enables developers to track the performance of critical code components, detect regressions, and so on.

However, access to the same accurate timing information can sometimes be also used for malicious purposes by an attacker to guess and infer data that they can't see or access otherwise. For example, cache attacks, statistical fingerprinting and micro-architectural attacks are a privacy and security concern where a malicious web site may use high resolution timing data of various browser or application-initiated operations to differentiate between subset of users, identify a particular user or reveal unrelated but same-process user data - see \[[CACHE-ATTACKS](https://w3c.github.io/hr-time/#bib-cache-attacks "The Spy in the Sandbox - Practical Cache Attacks in Javascript")\] and \[[SPECTRE](https://w3c.github.io/hr-time/#bib-spectre "Spectre Attacks: Exploiting Speculative Execution")\] for more background.

This specification defines an API that provides sub-millisecond time resolution, which is more accurate than the previously available millisecond resolution exposed by [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp). However, even without this new API an attacker may be able to obtain high-resolution estimates through repeat execution and statistical analysis.

tests: 1

-   [timing-attack](https://wpt.live/hr-time/timing-attack.html)

To ensure that the new API does not significantly improve the accuracy or speed of such attacks, the minimum resolution of the [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type should be inaccurate enough to prevent attacks.

Where necessary, the user agent should set higher resolution values to time resolution in [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time)'s processing model, to address privacy and security concerns due to architecture or software constraints, or other considerations.

In order to mitigate such attacks user agents may deploy any technique they deem necessary. Deployment of those techniques may vary based on the browser's architecture, the user's device, the content and its ability to maliciously read cross-origin data, or other practical considerations.

These techniques may include:

-   Resolution reduction.
-   Added jitter.
-   Abuse detection and/or API call throttling.

Mitigating such timing side-channel attacks entirely is practically impossible: either all operations would have to execute in a time that does not vary based on the value of any confidential information, or the application would need to be isolated from any time-related primitives (clock, timers, counters, etc). Neither is practical due to the associated complexity for the browser and application developers and the associated negative effects on performance and responsiveness of applications.

Note

Clock resolution is an unsolved and evolving area of research, with no existing industry consensus or definitive set of recommendations that applies to all browsers. To track the discussion, refer to [Issue 79](https://github.com/w3c/hr-time/issues/79).

This specification also defines an API that provides sub-millisecond time resolution of the zero time of the time origin, which requires and exposes a [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) to the application, and that must be shared across all the browser contexts. The [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) does not need to be tied to physical time, but is recommended to be set with respect to the \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] definition of [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range) to avoid exposing new fingerprint entropy about the user — e.g. this time can already be easily obtained by the application, whereas exposing a new logical clock provides new information.

However, even with the above mechanism in place, the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) may provide additional [clock drift](https://en.wikipedia.org/wiki/Clock_drift) resolution. Today, the application can timestamp the time-of-day and monotonic time values (via [`Date.now()`](https://tc39.es/ecma262/multipage/#sec-date.now) and [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()`) at multiple points within the same context and observe drift between them—e.g. due to automatic or user clock adjustments. With the [`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute, the attacker can also compare the [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin), as reported by the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock), against the current time-of-day estimate of the [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) (i.e. the difference between `performance.timeOrigin` and `Date.now() - performance.now()`) and potentially observe clock drift between these clocks over a longer time period.

In practice, the same time drift can be observed by an application across multiple navigations: the application can record the logical time in each context and use a client or server time synchronization mechanism to infer changes in the user's clock. Similarly, lower-layer mechanisms such as TCP timestamps may reveal the same high-resolution information to the server without the need for multiple visits. As such, the information provided by this API should not expose any significant or previously unavailable entropy about the user.

The current definition of [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) for a [`Document`](https://dom.spec.whatwg.org/#document) exposes the total time of cross-origin redirects prior to the request arriving at the document's origin. This exposes cross-origin information, however it's not yet decided how to mitigate this without causing major breakages to performance metrics.

To track the discussion, refer to [Navigation Timing Issue 160](https://github.com/w3c/navigation-timing/issues/160).

As well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative.

The key words _MUST_ and _SHOULD_ in this document are to be interpreted as described in [BCP 14](https://datatracker.ietf.org/doc/html/bcp14) \[[RFC2119](https://w3c.github.io/hr-time/#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://w3c.github.io/hr-time/#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

Some conformance requirements are phrased as requirements on attributes, methods or objects. Such requirements are to be interpreted as requirements on user agents.

-   [clock](https://w3c.github.io/hr-time/#dfn-clock)
-   [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time)
-   [coarsened moments](https://w3c.github.io/hr-time/#dfn-moment)
-   [coarsened shared current time](https://w3c.github.io/hr-time/#dfn-coarsened-shared-current-time)
-   [current high resolution time](https://w3c.github.io/hr-time/#dfn-current-high-resolution-time)
-   [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time)
-   [current relative timestamp](https://w3c.github.io/hr-time/#dfn-current-relative-timestamp)
-   current wall time
    -   [definition of](https://w3c.github.io/hr-time/#dfn-current-wall-time)
    -   [definition of](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time)
-   [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)
-   [duration](https://w3c.github.io/hr-time/#dfn-duration)
-   [duration from](https://w3c.github.io/hr-time/#dfn-duration-from)
-   [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp)
-   [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch)
-   [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp)
-   [implicitly convert a duration to a timestamp](https://w3c.github.io/hr-time/#dfn-implicitly-convert-a-duration-to-a-timestamp)
-   [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)
-   [`now()`](https://w3c.github.io/hr-time/#dom-performance-now) method for `Performance`
-   [`performance`](https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance) attribute for `WindowOrWorkerGlobalScope`
-   [`Performance`](https://w3c.github.io/hr-time/#dom-performance) interface
-   [relative high resolution coarse time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-coarse-time)
-   [relative high resolution time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-time)
-   [`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute for `Performance`
-   [`toJSON()`](https://w3c.github.io/hr-time/#dom-performance-tojson) method for `Performance`
-   [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch)
-   unsafe current time
    -   [definition of](https://w3c.github.io/hr-time/#dfn-unsafe-current-time)
    -   [definition of](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time)
    -   [definition of](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time)
-   [unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment)
-   [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time)
-   [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)

-   \[[DOM](https://w3c.github.io/hr-time/#bib-dom)\] defines the following:
    -   `Document` interface
    -   `EventTarget` interface
    -   `timeStamp` attribute (for `Event`)
-   \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262)\] defines the following:
    -   Date
    -   Date.now()
    -   time
-   \[[HTML](https://w3c.github.io/hr-time/#bib-html)\] defines the following:
    -   `BroadcastChannel` interface
    -   cross-origin isolated capability (for environment settings object)
    -   environment settings object
    -   familiar with
    -   global object
    -   global object (for `realm`)
    -   navigate
    -   parse a duration string
    -   `postMessage(message, options)` (for `Window`)
    -   relevant global object
    -   relevant settings object
    -   run a worker
    -   `SharedWorker` interface
    -   time origins (for environment settings object)
    -   `Window` interface
    -   `WindowOrWorkerGlobalScope` interface
    -   `Worker` interface
-   \[[INFRA](https://w3c.github.io/hr-time/#bib-infra)\] defines the following:
    -   implementation-defined
    -   tracking vector
    -   user agent
-   \[[REPORTING](https://w3c.github.io/hr-time/#bib-reporting)\] defines the following:
    -   generation time
-   \[[SERVICE-WORKERS](https://w3c.github.io/hr-time/#bib-service-workers)\] defines the following:
    -   `ServiceWorker` interface
-   \[[TEMPORAL](https://w3c.github.io/hr-time/#bib-temporal)\] defines the following:
    -   Temporal.Instant
-   \[[WEBIDL](https://w3c.github.io/hr-time/#bib-webidl)\] defines the following:
    -   `[Default]` extended attribute
    -   default toJSON steps
    -   `double` type
    -   `[Exposed]` extended attribute
    -   `object` type
    -   `[Replaceable]` extended attribute
    -   this
    -   `unsigned long long` type

```
<span data-idl="" data-title="DOMHighResTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-double" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-double" id="ref-for-index-term-double-type-3">double<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-13"><code>DOMHighResTimeStamp<!---0.544438%--></code></a>;<!---0.544438%--></span>

<span data-idl="" data-title="EpochTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-unsigned-long-long" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-unsigned-long-long" id="ref-for-index-term-unsigned-long-long-type-2">unsigned long long<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-epochtimestamp" id="ref-for-dom-epochtimestamp-4"><code>EpochTimeStamp<!---0.544438%--></code></a>;<!---0.544438%--></span>

<span data-idl="" data-title="Performance">[<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Exposed" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Exposed" id="ref-for-index-term-exposed-extended-attribute-2">Exposed<!---0.544438%--></a>=(Window,Worker)<!---0.544438%--></span>]
interface <a data-link-for="" data-link-type="interface" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-9"><code>Performance<!---0.544438%--></code></a> : <span><a data-link-type="idl" data-xref-type="_IDL_" data-cite="dom" data-cite-path="/" data-cite-frag="eventtarget" data-type="interface" href="https://dom.spec.whatwg.org/#eventtarget" id="ref-for-index-term-eventtarget-interface-2">EventTarget<!---0.544438%--></a><!---0.544438%--></span> {<span data-idl="" data-title="now" data-dfn-for="Performance"><span>
    <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-14"><code>DOMHighResTimeStamp<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-now" id="ref-for-dom-performance-now-6"><code>now<!---0.544438%--></code></a>();<!---0.544438%--></span><span data-idl="" data-title="timeOrigin" data-dfn-for="Performance">
    readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-15"><code>DOMHighResTimeStamp<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-performance-timeorigin" id="ref-for-dom-performance-timeorigin-6"><code>timeOrigin<!---0.544438%--></code></a>;<!---0.544438%--></span><span data-idl="" data-title="toJSON" data-dfn-for="Performance">
    [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Default" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Default" id="ref-for-index-term-default-extended-attribute-2">Default<!---0.544438%--></a><!---0.544438%--></span>]<span> <a data-link-type="interface" data-xref-type="interface" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-object" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-object" id="ref-for-index-term-object-type-2">object<!---0.544438%--></a><!---0.544438%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-tojson" id="ref-for-dom-performance-tojson-2"><code>toJSON<!---0.544438%--></code></a>();<!---0.544438%--></span>
};<!---0.544438%--></span>

<span data-idl="" data-title="WindowOrWorkerGlobalScope">partial interface mixin <a data-idl="partial" data-link-type="interface" data-title="WindowOrWorkerGlobalScope" data-xref-type="interface" data-dfn-for="WindowOrWorkerGlobalScope" data-cite="html" data-cite-path="/webappapis.html" data-cite-frag="windoworworkerglobalscope" data-type="interface" href="https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope" id="ref-for-index-term-windoworworkerglobalscope-interface-3">WindowOrWorkerGlobalScope<!---0.544438%--></a> {<span data-idl="" data-title="performance" data-dfn-for="WindowOrWorkerGlobalScope">
  [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Replaceable" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Replaceable" id="ref-for-index-term-replaceable-extended-attribute-2">Replaceable<!---0.544438%--></a><!---0.544438%--></span>] readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-10"><code>Performance<!---0.544438%--></code></a><!---0.544438%--></span> <a data-link-for="WindowOrWorkerGlobalScope" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance" id="ref-for-dom-windoworworkerglobalscope-performance-2"><code>performance<!---0.544438%--></code></a>;<!---0.544438%--></span>
};<!---0.544438%--></span>
```

Thanks to Arvind Jain, Angelos D. Keromytis, Boris Zbarsky, Jason Weber, Karen Anderson, Nat Duca, Philippe Le Hegaret, Ryosuke Niwa, Simha Sethumadhavan, Todd Reifsteck, Tony Gentilcore, Vasileios P. Kemerlis, Yoav Weiss, and Yossef Oren for their contributions to this work.

\[dom\]

[DOM Standard](https://dom.spec.whatwg.---
created: 2024-08-23T05:14:32 (UTC -07:00)
tags: []
source: https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time
author: Yoav Weiss (Google LLC)
---

# High Resolution Time

> ## Excerpt
> This specification defines an API that provides the time origin, and
        current time in sub-millisecond resolution, such that it is not subject
        to system clock skew or adjustments.

---
## Abstract

This specification defines an API that provides the time origin, and current time in sub-millisecond resolution, such that it is not subject to system clock skew or adjustments.

## Status of This Document

_This section describes the status of this document at the time of its publication. A list of current W3C publications and the latest revision of this technical report can be found in the [W3C technical reports index](https://www.w3.org/TR/) at https://www.w3.org/TR/._

This document was published by the [Web Performance Working Group](https://www.w3.org/groups/wg/webperf) as an Editor's Draft.

Publication as an Editor's Draft does not imply endorsement by W3C and its Members.

This is a draft document and may be updated, replaced or obsoleted by other documents at any time. It is inappropriate to cite this document as other than work in progress.

This document was produced by a group operating under the [W3C Patent Policy](https://www.w3.org/policies/patent-policy/). W3C maintains a [public list of any patent disclosures](https://www.w3.org/groups/wg/webperf/ipr) made in connection with the deliverables of the group; that page also includes instructions for disclosing a patent. An individual who has actual knowledge of a patent which the individual believes contains [Essential Claim(s)](https://www.w3.org/policies/patent-policy/#def-essential) must disclose the information in accordance with [section 6 of the W3C Patent Policy](https://www.w3.org/policies/patent-policy/#sec-Disclosure).

This document is governed by the [03 November 2023 W3C Process Document](https://www.w3.org/policies/process/20231103/).

## Table of Contents

1.  [Abstract](https://w3c.github.io/hr-time/#abstract)
2.  [Status of This Document](https://w3c.github.io/hr-time/#sotd)
3.  [1. Introduction](https://w3c.github.io/hr-time/#introduction)
    1.  [1.1 Use-cases](https://w3c.github.io/hr-time/#use-cases)
    2.  [1.2 Examples](https://w3c.github.io/hr-time/#examples)
4.  [2. Time Concepts](https://w3c.github.io/hr-time/#sec-concepts)
    1.  [2.1 Clocks](https://w3c.github.io/hr-time/#sec-clocks)
    2.  [2.2 Moments and Durations](https://w3c.github.io/hr-time/#moments-and-durations)
5.  [3. Tools for Specification Authors](https://w3c.github.io/hr-time/#sec-tools)
    1.  [3.1 Examples](https://w3c.github.io/hr-time/#sec-tools-examples)
6.  [4. Time Origin](https://w3c.github.io/hr-time/#sec-time-origin)
7.  [5. The `DOMHighResTimeStamp` typedef](https://w3c.github.io/hr-time/#sec-domhighrestimestamp)
8.  [6. The `EpochTimeStamp` typedef](https://w3c.github.io/hr-time/#the-epochtimestamp-typedef)
9.  [7. The `Performance` interface](https://w3c.github.io/hr-time/#sec-performance)
    1.  [7.1 `now()` method](https://w3c.github.io/hr-time/#now-method)
    2.  [7.2 `timeOrigin` attribute](https://w3c.github.io/hr-time/#timeorigin-attribute)
    3.  [7.3 `toJSON()` method](https://w3c.github.io/hr-time/#tojson-method)
10.  [8. Extensions to `WindowOrWorkerGlobalScope` mixin](https://w3c.github.io/hr-time/#extensions-to-windoworworkerglobalscope-mixin)
    1.  [8.1 The `performance` attribute](https://w3c.github.io/hr-time/#the-performance-attribute)
11.  [9. Security Considerations](https://w3c.github.io/hr-time/#sec-security)
    1.  [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution)
    2.  [9.2 Clock drift](https://w3c.github.io/hr-time/#clock-drift)
12.  [10. Privacy Considerations](https://w3c.github.io/hr-time/#sec-privacy)
13.  [11. Conformance](https://w3c.github.io/hr-time/#conformance)
14.  [A. Index](https://w3c.github.io/hr-time/#index)
    1.  [A.1 Terms defined by this specification](https://w3c.github.io/hr-time/#index-defined-here)
    2.  [A.2 Terms defined by reference](https://w3c.github.io/hr-time/#index-defined-elsewhere)
15.  [B. IDL Index](https://w3c.github.io/hr-time/#idl-index)
16.  [C. Acknowledgments](https://w3c.github.io/hr-time/#acknowledgments)
17.  [D. References](https://w3c.github.io/hr-time/#references)
    1.  [D.1 Normative references](https://w3c.github.io/hr-time/#normative-references)
    2.  [D.2 Informative references](https://w3c.github.io/hr-time/#informative-references)

_This section is non-normative._

The ECMAScript Language specification \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] defines the `[Date](https://tc39.es/ecma262/multipage/#sec-date-objects)` object as a time value representing time in milliseconds since 01 January, 1970 UTC. For most purposes, this definition of time is sufficient as these values represent time to millisecond precision for any moment that is within approximately 285,616 years from 01 January, 1970 UTC.

In practice, these definitions of time are subject to both clock skew and adjustment of the system clock. The value of time may not always be monotonically increasing and subsequent values may either decrease or remain the same.

For example, the following script may record a positive number, negative number, or zero for computed `duration`:

[Example 1](https://w3c.github.io/hr-time/#example-1)

```
<span>var</span> mark_start = <span>Date</span>.now();
doTask(); <span>// Some task</span>
<span>var</span> duration = <span>Date</span>.now() - mark_start;
```

For certain tasks this definition of time may not be sufficient as it:

-   Does not have a stable monotonic clock, and as a result, it is subject to system clock skew.
-   Does not provide sub-millisecond time resolution.

This specification does not propose changing the behavior of `[Date.now()](https://tc39.es/ecma262/multipage/#sec-date.now)` \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] as it is genuinely useful in determining the current value of the calendar time and has a long history of usage. The [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type, [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method, and [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attributes of the [`Performance`](https://w3c.github.io/hr-time/#dom-performance) interface resolve the above issues by providing monotonically increasing time values with sub-millisecond resolution.

Note

Providing sub-millisecond resolution is not a mandatory part of this specification. Implementations may choose to limit the timer resolution they expose for privacy and security reasons, and not expose sub-millisecond timers. Use-cases that rely on sub-millisecond resolution may not be satisfied when that happens.

_This section is non-normative._

This specification defines a few different capabilities: it provides timestamps based on a stable, monotonic clock, comparable across contexts, with potential sub-millisecond resolution.

The need for a stable monotonic clock when talking about performance measurements stems from the fact that unrelated clock skew can distort measurements and render them useless. For example, when attempting to accurately measure the elapsed time of navigating to a Document, fetching of resources or execution of script, a monotonically increasing clock with sub-millisecond resolution is desired.

Comparing timestamps between contexts is essential e.g. when synchronizing work between a [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker) and the main thread or when instrumenting such work in order to create a unified view of the event timeline.

Finally, the need for sub-millisecond timers revolves around the following use-cases:

-   Ability to schedule work in sub-millisecond intervals. That is particularly important on the main thread, where work can interfere with frame rendering which needs to happen in short and regular intervals, to avoid user-visible jank.
-   When calculating the frame rate of a script-based animation, developers will need sub-millisecond resolution in order to determine if an animation is drawing at 60 FPS. Without sub-millisecond resolution, a developer can only determine if an animation is drawing at 58.8 FPS (1000ms / 16) or 62.5 FPS (1000ms / 17).
-   When collecting in-the-wild measurements of JS code (e.g. using User-Timing), developers may be interested in gathering sub-milliseconds timing of their functions, to catch regressions early.
-   When attempting to cue audio to a specific point in an animation or ensure that the audio and animation are perfectly synchronized, developers will need to accurately measure the amount of time elapsed.

_This section is non-normative._

A developer may wish to construct a timeline of their entire application, including events from [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker) or [`SharedWorker`](https://html.spec.whatwg.org/multipage/workers.html#sharedworker), which have different [time origins](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin). To display such events on the same timeline, the application can translate the [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)s with the help of the [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute.

[Example 2](https://w3c.github.io/hr-time/#example-2)

```
<span>// ---- worker.js -----------------------------</span>
<span>// Shared worker script</span>
onconnect = <span><span>function</span>(<span>e</span>) </span>{
  <span>var</span> port = e.ports[<span>0</span>];
  port.onmessage = <span><span>function</span>(<span>e</span>) </span>{
    <span>// Time execution in worker</span>
    <span>var</span> task_start = performance.now();
    result = runSomeWorkerTask();
    <span>var</span> task_end = performance.now();
  }

  <span>// Send results and epoch-relative timestamps to another context</span>
  port.postMessage({
    <span>'task'</span>: <span>'Some worker task'</span>,
    <span>'start_time'</span>: task_start + performance.timeOrigin,
    <span>'end_time'</span>: task_end + performance.timeOrigin,
    <span>'result'</span>: result
  });
}

<span>// ---- application.js ------------------------</span>
<span>// Timing tasks in the document</span>
<span>var</span> task_start = performance.now();
runSomeApplicationTask();
<span>var</span> task_end = performance.now();

<span>// developer provided method to upload runtime performance data</span>
reportEventToAnalytics({
  <span>'task'</span>: <span>'Some document task'</span>,
  <span>'start_time'</span>: task_start,
  <span>'duration'</span>: task_end - task_start
});

<span>// Translating worker timestamps into document's time origin</span>
<span>var</span> worker = <span>new</span> SharedWorker(<span>'worker.js'</span>);
worker.port.onmessage = <span><span>function</span> (<span>event</span>) </span>{
  <span>var</span> msg = event.data;

  <span>// translate epoch-relative timestamps into document's time origin</span>
  msg.start_time = msg.start_time - performance.timeOrigin;
  msg.end_time = msg.end_time - performance.timeOrigin;

  reportEventToAnalytics(msg);
}
```

A clock tracks the passage of time and can report the unsafe current time that an algorithm step is executing. There are many kinds of clocks. All clocks on the web platform attempt to count 1 millisecond of clock time per 1 millisecond of real-world time, but they differ in how they handle cases where they can't be exactly correct.

-   The wall clock's unsafe current time is always as close as possible to a user's notion of time. Since a computer sometimes runs slow or fast or loses track of time, its [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) sometimes needs to be adjusted, which means the [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time) can decrease, making it unreliable for performance measurement or recording the orders of events. The web platform shares a [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) with \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range).
-   The monotonic clock's unsafe current time never decreases, so it can't be changed by system clock adjustments. The [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) only exists within a single execution of the [user agent](https://infra.spec.whatwg.org/#user-agent), so it can't be used to compare events that might happen in different executions.
    
    Note
    
    Since the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) can't be adjusted to match the user's notion of time, it should be used for measurement, rather than user-visible times. For any time communication with the user, use the wall clock.
    
    Note
    
    The user agent can pick a new [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) when the browser restarts, when it starts an isolated browsing session—e.g. incognito or a similar browsing mode—or when it creates an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) that can't communicate with any existing settings objects. As a result, developers should not use shared timestamps as absolute time that holds its monotonic properties across all past, present, and future contexts; in practice, the monotonic properties only apply for contexts that can reach each other by exchanging messages via one of the provided messaging mechanisms - e.g. [`postMessage`](https://html.spec.whatwg.org/multipage/web-messaging.html#dom-window-postmessage-options)`(message, options)`, [`BroadcastChannel`](https://html.spec.whatwg.org/multipage/web-messaging.html#broadcastchannel), etc.
    
    Note
    
    In certain scenarios (e.g. when a tab is backgrounded), the user agent may choose to throttle timers and periodic callbacks run in that context or even freeze them entirely. Any such throttling should not affect the resolution or accuracy of the time returned by the monotonic clock.
    

Each [clock](https://w3c.github.io/hr-time/#dfn-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#dfn-unsafe-current-time) returns an unsafe moment. [Coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) converts these [unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) to coarsened moments or just [moments](https://w3c.github.io/hr-time/#dfn-moment). [Unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) and [moments](https://w3c.github.io/hr-time/#dfn-moment) from different clocks are not comparable.

Note

[Moments](https://w3c.github.io/hr-time/#dfn-moment) and [unsafe moments](https://w3c.github.io/hr-time/#dfn-unsafe-moment) represent points in time, which means they can't be directly stored as numbers. Implementations will usually represent a [moment](https://w3c.github.io/hr-time/#dfn-moment) as a [duration](https://w3c.github.io/hr-time/#dfn-duration) from some other fixed point in time, but specifications ought to deal in the [moments](https://w3c.github.io/hr-time/#dfn-moment) themselves.

A duration is the distance from one [moment](https://w3c.github.io/hr-time/#dfn-moment) to another from the same [clock](https://w3c.github.io/hr-time/#dfn-clock). Neither endpoint can be an [unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment) so that both [durations](https://w3c.github.io/hr-time/#dfn-duration) and differences of [durations](https://w3c.github.io/hr-time/#dfn-duration) mitigate the concerns in [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution). [Durations](https://w3c.github.io/hr-time/#dfn-duration) are measured in milliseconds, seconds, etc. Since all [clocks](https://w3c.github.io/hr-time/#dfn-clock) attempt to count at the same rate, [durations](https://w3c.github.io/hr-time/#dfn-duration) don't have an associated [clock](https://w3c.github.io/hr-time/#dfn-clock), and a [duration](https://w3c.github.io/hr-time/#dfn-duration) calculated from two [moments](https://w3c.github.io/hr-time/#dfn-moment) on one clock can be added to a [moment](https://w3c.github.io/hr-time/#dfn-moment) from a second [clock](https://w3c.github.io/hr-time/#dfn-clock), to produce another [moment](https://w3c.github.io/hr-time/#dfn-moment) on that second [clock](https://w3c.github.io/hr-time/#dfn-clock).

The duration from a to b is the result of the following algorithm:

1.  [Assert](https://infra.spec.whatwg.org/#assert): a was created by the same [clock](https://w3c.github.io/hr-time/#dfn-clock) as b.
2.  [Assert](https://infra.spec.whatwg.org/#assert): Both a and b are [coarsened moments](https://w3c.github.io/hr-time/#dfn-moment).
3.  Return the amount of time from a to b as a [duration](https://w3c.github.io/hr-time/#dfn-duration). If b came before a, this will be a negative [duration](https://w3c.github.io/hr-time/#dfn-duration).

[Durations](https://w3c.github.io/hr-time/#dfn-duration) can be used implicitly as [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)s. To implicitly convert a duration to a timestamp, given a [duration](https://w3c.github.io/hr-time/#dfn-duration) d, return the number of milliseconds in d.

For measuring time within a single page (within the context of a single [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)), use the settingsObject's current relative timestamp, defined as the [duration from](https://w3c.github.io/hr-time/#dfn-duration-from) settingsObject's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) to the settingsObject's [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time). This value can be exposed directly to JavaScript using the [duration](https://w3c.github.io/hr-time/#dfn-duration)'s [implicit conversion](https://w3c.github.io/hr-time/#dfn-implicitly-convert-a-duration-to-a-timestamp) to [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp).

For measuring time within a single UA execution when an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) isn't an appropriate base for comparison, create [moments](https://w3c.github.io/hr-time/#dfn-moment) using an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time). An [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) settingsObject's current monotonic time is the result of the following steps:

1.  Let unsafeMonotonicTime be the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time).
2.  Return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with unsafeMonotonicTime and settingsObject's [cross-origin isolated capability](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability).

[Moments](https://w3c.github.io/hr-time/#dfn-moment) from the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) can't be directly represented in JavaScript or HTTP. Instead, expose a [duration](https://w3c.github.io/hr-time/#dfn-duration) between two such [moments](https://w3c.github.io/hr-time/#dfn-moment).

For measuring time across multiple UA executions, create [moments](https://w3c.github.io/hr-time/#dfn-moment) using the [current wall time](https://w3c.github.io/hr-time/#dfn-current-wall-time) or (if you need higher precision in [cross-origin-isolated contexts](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability)) an [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time). The current wall time is the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).

An [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) settingsObject's current wall time is the result of the following steps:

1.  Let unsafeWallTime be the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).
2.  Return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with unsafeWallTime and settingsObject's [cross-origin isolated capability](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-cross-origin-isolated-capability).

When using [moments](https://w3c.github.io/hr-time/#dfn-moment) from the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock), be sure that your design accounts for situations when the user adjusts their clock either forward or backward.

[Moments](https://w3c.github.io/hr-time/#dfn-moment) from the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) can be represented in JavaScript by passing the number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to that [moment](https://w3c.github.io/hr-time/#dfn-moment) into the [`` `Date` ``](https://tc39.es/ecma262/multipage/#sec-date-objects) constructor, or by passing the number of nanoseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to that [moment](https://w3c.github.io/hr-time/#dfn-moment) into the [Temporal.Instant](https://tc39.es/proposal-temporal/#sec-temporal-instant-constructor) constructor.

Avoid sending similar representations between computers, as doing so will expose the user's clock skew, which is a [tracking vector](https://infra.spec.whatwg.org/#tracking-vector). Instead, use an approach similar to [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) [moments](https://w3c.github.io/hr-time/#dfn-moment) of sending a duration between two [moments](https://w3c.github.io/hr-time/#dfn-moment).

The age of an error report can be computed using:

7.  Initialize report's [generation time](https://www.w3.org/TR/reporting-1/#report-timestamp) to settings' [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time).

Later:

2.  Let data be a map with the following key/value pairs:
    
    age
    
    The number of milliseconds between report's [generation time](https://www.w3.org/TR/reporting-1/#report-timestamp) and context's [relevant settings object](https://html.spec.whatwg.org/multipage/webappapis.html#relevant-settings-object)'s [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time), rounded to the nearest integer.
    
    ...
    

Multi-day attribution report expirations can be handled as:

2.  Let source be a new attribution source struct whose items are:
    
    ...
    
    source time
    
    context's [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time)
    
    expiry
    
    [parse a duration string](https://html.spec.whatwg.org/multipage/#parse-a-duration-string) from `value["expiry"]`
    

Days later:

2.  If context's [current wall time](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time) is less than source's source time + source's expiry, send a report.

The Unix epoch is the [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock) corresponding to 1 January 1970 00:00:00 UTC.

Each group of [environment settings objects](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object) that could possibly communicate in any way has an estimated monotonic time of the Unix epoch, a [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock), whose value is initialized by the following steps:

1.  Let wall time be the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time).
2.  Let monotonic time be the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)'s [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time).
3.  Let epoch time be `monotonic time - (wall time - [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch))`
4.  Initialize the [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) to the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with epoch time.

Issue 1

The above set of settings-objects-that-could-possibly-communicate needs to be specified better. It's similar to [familiar with](https://html.spec.whatwg.org/multipage/browsers.html#familiar-with) but includes [`Worker`](https://html.spec.whatwg.org/multipage/workers.html#worker)

s.

Performance measurements report a [duration](https://w3c.github.io/hr-time/#dfn-duration) from a [moment](https://w3c.github.io/hr-time/#dfn-moment) early in the initialization of a relevant [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object). That [moment](https://w3c.github.io/hr-time/#dfn-moment) is stored in that settings object's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).

To get time origin timestamp, given a [global object](https://html.spec.whatwg.org/multipage/webappapis.html#global-object) global, run the following steps, which return a [duration](https://w3c.github.io/hr-time/#dfn-duration):

1.  Let timeOrigin be global's [relevant settings object](https://html.spec.whatwg.org/multipage/webappapis.html#relevant-settings-object)'s [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).
    
2.  Return the [duration from](https://w3c.github.io/hr-time/#dfn-duration-from) the [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch) to timeOrigin.

Note

The value returned by [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp) is approximately the time after the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) that global's [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) happened. It may differ from the value returned by [`Date.now()`](https://tc39.es/ecma262/multipage/#sec-date.now) executed at the time origin, because the former is recorded with respect to a [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) that is not subject to system and user clock adjustments, clock skew, and so on.

The coarsen time algorithm, given an

[unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment)

timestamp on some

[clock](https://w3c.github.io/hr-time/#dfn-clock)

and an optional boolean crossOriginIsolatedCapability (default false), runs the following steps:

1.  Let time resolution be 100 microseconds, or a higher [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) value.
2.  If crossOriginIsolatedCapability is true, set time resolution to be 5 microseconds, or a higher [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) value.
3.  In an [implementation-defined](https://infra.spec.whatwg.org/#implementation-defined) manner, coarsen and potentially jitter timestamp such that its resolution will not exceed time resolution.
4.  Return timestamp as a [moment](https://w3c.github.io/hr-time/#dfn-moment).

The current high resolution time given a [global object](https://html.spec.whatwg.org/multipage/webappapis.html#global-object) current global must return the result of [relative high resolution time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-time) given [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time) and current global.

The coarsened shared current time given an optional boolean crossOriginIsolatedCapability (default false), must return the result of calling [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time) with the [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time) and crossOriginIsolatedCapability.

The unsafe shared current time must return the [unsafe current time](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time) of the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock).

The [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type is used to store a [duration](https://w3c.github.io/hr-time/#dfn-duration) in milliseconds. Depending on its context, it may represent the [moment](https://w3c.github.io/hr-time/#dfn-moment) that is this [duration](https://w3c.github.io/hr-time/#dfn-duration) after a base [moment](https://w3c.github.io/hr-time/#dfn-moment) like a [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) or the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch).

```
<span data-idl="" id="idl-def-domhighrestimestamp" data-title="DOMHighResTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-double" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-double" id="ref-for-index-term-double-type-1">double<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-6"><code>DOMHighResTimeStamp<!---0.176915%--></code></a>;<!---0.176915%--></span><!---0.176915%-->
```

A [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) _SHOULD_ represent a time in milliseconds accurate enough to allow measurement while preventing timing attacks - see [9.1 Clock resolution](https://w3c.github.io/hr-time/#clock-resolution) for additional considerations.

Note

A [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) is a [`double`](https://webidl.spec.whatwg.org/#idl-double), so it can only represent an epoch-relative time—the number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to a [moment](https://w3c.github.io/hr-time/#dfn-moment)—to a finite resolution. For [moments](https://w3c.github.io/hr-time/#dfn-moment) in 2023, that resolution is approximately 0.2 microseconds.

```
<span data-idl="" id="idl-def-epochtimestamp" data-title="EpochTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-unsigned-long-long" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-unsigned-long-long" id="ref-for-index-term-unsigned-long-long-type-1">unsigned long long<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-epochtimestamp" id="ref-for-dom-epochtimestamp-1"><code>EpochTimeStamp<!---0.176915%--></code></a>;<!---0.176915%--></span><!---0.176915%-->
```

Note

: Legacy platform feature

A [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp) represents an integral number of milliseconds from the [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch) to a given [moment](https://w3c.github.io/hr-time/#dfn-moment) on the [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock), excluding leap seconds. Specifications that use this type define how the number of milliseconds are interpreted.

```
<span data-idl="" id="idl-def-performance" data-title="Performance">[<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Exposed" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Exposed" id="ref-for-index-term-exposed-extended-attribute-1">Exposed<!---0.176915%--></a>=(Window,Worker)<!---0.176915%--></span>]
interface <a data-link-for="" data-link-type="interface" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-5"><code>Performance<!---0.176915%--></code></a> : <span><a data-link-type="idl" data-xref-type="_IDL_" data-cite="dom" data-cite-path="/" data-cite-frag="eventtarget" data-type="interface" href="https://dom.spec.whatwg.org/#eventtarget" id="ref-for-index-term-eventtarget-interface-1">EventTarget<!---0.176915%--></a><!---0.176915%--></span> {<span data-idl="" id="idl-def-performance-now" data-title="now" data-dfn-for="Performance"><span>
    <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-10"><code>DOMHighResTimeStamp<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-now" id="ref-for-dom-performance-now-2"><code>now<!---0.176915%--></code></a>();<!---0.176915%--></span><span data-idl="" id="idl-def-performance-timeorigin" data-title="timeOrigin" data-dfn-for="Performance">
    readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-11"><code>DOMHighResTimeStamp<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-performance-timeorigin" id="ref-for-dom-performance-timeorigin-3"><code>timeOrigin<!---0.176915%--></code></a>;<!---0.176915%--></span><span data-idl="" id="idl-def-performance-tojson" data-title="toJSON" data-dfn-for="Performance">
    [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Default" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Default" id="ref-for-index-term-default-extended-attribute-1">Default<!---0.176915%--></a><!---0.176915%--></span>]<span> <a data-link-type="interface" data-xref-type="interface" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-object" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-object" id="ref-for-index-term-object-type-1">object<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-tojson" id="ref-for-dom-performance-tojson-1"><code>toJSON<!---0.176915%--></code></a>();<!---0.176915%--></span>
};<!---0.176915%--></span><!---0.176915%-->
```

The `now()` method _MUST_ return the number of milliseconds in the [current high resolution time](https://w3c.github.io/hr-time/#dfn-current-high-resolution-time) given [this](https://webidl.spec.whatwg.org/#this)'s [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) (a [duration](https://w3c.github.io/hr-time/#dfn-duration)).

tests: 2

-   [basic](https://wpt.live/hr-time/basic.any.html)
-   [basic](https://wpt.live/hr-time/basic.any.worker.html)

The time values returned when calling the [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method on [`Performance`](https://w3c.github.io/hr-time/#dom-performance) objects with the same [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) _MUST_ use the same [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock). The difference between any two chronologically recorded time values returned from the [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()` method _MUST_ never be negative if the two time values have the same [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin).

tests: 2

-   [monotonic-clock](https://wpt.live/hr-time/monotonic-clock.any.html)
-   [monotonic-clock](https://wpt.live/hr-time/monotonic-clock.any.worker.html)

The `timeOrigin` attribute _MUST_ return the number of milliseconds in the [duration](https://w3c.github.io/hr-time/#dfn-duration) returned by [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp) for the [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) of [this](https://webidl.spec.whatwg.org/#this).

tests: 2

-   [timeOrigin](https://wpt.live/hr-time/timeOrigin.html)
-   [window-worker-timeOrigin](https://wpt.live/hr-time/window-worker-timeOrigin.window.html)

The time values returned when getting [`Performance`](https://w3c.github.io/hr-time/#dom-performance).[`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) _MUST_ use the same [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) that is shared by [time origins](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin), and whose reference point is the \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range) definition - see [9\. Security Considerations](https://w3c.github.io/hr-time/#sec-security).

tests: 1

-   [test\_cross\_frame\_start](https://wpt.live/hr-time/test_cross_frame_start.html)

When `toJSON()` is called, run \[[WEBIDL](https://w3c.github.io/hr-time/#bib-webidl "Web IDL Standard")\]'s [default toJSON steps](https://webidl.spec.whatwg.org/#default-tojson-steps).

tests: 1

-   [performance-tojson](https://wpt.live/hr-time/performance-tojson.html)

The `performance` attribute on the interface mixin [`WindowOrWorkerGlobalScope`](https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope) allows access to performance related attributes and methods from the [global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-realm-global).

```
<span data-idl="" id="idl-def-windoworworkerglobalscope-partial-1" data-title="WindowOrWorkerGlobalScope">partial interface mixin <a data-idl="partial" data-link-type="interface" data-title="WindowOrWorkerGlobalScope" data-xref-type="interface" data-dfn-for="WindowOrWorkerGlobalScope" data-cite="html" data-cite-path="/webappapis.html" data-cite-frag="windoworworkerglobalscope" data-type="interface" href="https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope" id="ref-for-index-term-windoworworkerglobalscope-interface-2">WindowOrWorkerGlobalScope<!---0.176915%--></a> {<span data-idl="" id="idl-def-windoworworkerglobalscope-performance" data-title="performance" data-dfn-for="WindowOrWorkerGlobalScope">
  [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Replaceable" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Replaceable" id="ref-for-index-term-replaceable-extended-attribute-1">Replaceable<!---0.176915%--></a><!---0.176915%--></span>] readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-8"><code>Performance<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="WindowOrWorkerGlobalScope" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance" id="ref-for-dom-windoworworkerglobalscope-performance-1"><code>performance<!---0.176915%--></code></a>;<!---0.176915%--></span>
};<!---0.176915%--></span><!---0.176915%-->
```

Access to accurate timing information, both for measurement and scheduling purposes, is a common requirement for many applications. For example, coordinating animations, sound, and other activity on the page requires access to high-resolution time to provide a good user experience. Similarly, measurement enables developers to track the performance of critical code components, detect regressions, and so on.

However, access to the same accurate timing information can sometimes be also used for malicious purposes by an attacker to guess and infer data that they can't see or access otherwise. For example, cache attacks, statistical fingerprinting and micro-architectural attacks are a privacy and security concern where a malicious web site may use high resolution timing data of various browser or application-initiated operations to differentiate between subset of users, identify a particular user or reveal unrelated but same-process user data - see \[[CACHE-ATTACKS](https://w3c.github.io/hr-time/#bib-cache-attacks "The Spy in the Sandbox - Practical Cache Attacks in Javascript")\] and \[[SPECTRE](https://w3c.github.io/hr-time/#bib-spectre "Spectre Attacks: Exploiting Speculative Execution")\] for more background.

This specification defines an API that provides sub-millisecond time resolution, which is more accurate than the previously available millisecond resolution exposed by [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp). However, even without this new API an attacker may be able to obtain high-resolution estimates through repeat execution and statistical analysis.

tests: 1

-   [timing-attack](https://wpt.live/hr-time/timing-attack.html)

To ensure that the new API does not significantly improve the accuracy or speed of such attacks, the minimum resolution of the [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp) type should be inaccurate enough to prevent attacks.

Where necessary, the user agent should set higher resolution values to time resolution in [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time)'s processing model, to address privacy and security concerns due to architecture or software constraints, or other considerations.

In order to mitigate such attacks user agents may deploy any technique they deem necessary. Deployment of those techniques may vary based on the browser's architecture, the user's device, the content and its ability to maliciously read cross-origin data, or other practical considerations.

These techniques may include:

-   Resolution reduction.
-   Added jitter.
-   Abuse detection and/or API call throttling.

Mitigating such timing side-channel attacks entirely is practically impossible: either all operations would have to execute in a time that does not vary based on the value of any confidential information, or the application would need to be isolated from any time-related primitives (clock, timers, counters, etc). Neither is practical due to the associated complexity for the browser and application developers and the associated negative effects on performance and responsiveness of applications.

Note

Clock resolution is an unsolved and evolving area of research, with no existing industry consensus or definitive set of recommendations that applies to all browsers. To track the discussion, refer to [Issue 79](https://github.com/w3c/hr-time/issues/79).

This specification also defines an API that provides sub-millisecond time resolution of the zero time of the time origin, which requires and exposes a [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) to the application, and that must be shared across all the browser contexts. The [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) does not need to be tied to physical time, but is recommended to be set with respect to the \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262 "ECMAScript Language Specification")\] definition of [time](https://tc39.es/ecma262/multipage/#sec-time-values-and-time-range) to avoid exposing new fingerprint entropy about the user — e.g. this time can already be easily obtained by the application, whereas exposing a new logical clock provides new information.

However, even with the above mechanism in place, the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock) may provide additional [clock drift](https://en.wikipedia.org/wiki/Clock_drift) resolution. Today, the application can timestamp the time-of-day and monotonic time values (via [`Date.now()`](https://tc39.es/ecma262/multipage/#sec-date.now) and [`now`](https://w3c.github.io/hr-time/#dom-performance-now)`()`) at multiple points within the same context and observe drift between them—e.g. due to automatic or user clock adjustments. With the [`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute, the attacker can also compare the [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin), as reported by the [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock), against the current time-of-day estimate of the [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) (i.e. the difference between `performance.timeOrigin` and `Date.now() - performance.now()`) and potentially observe clock drift between these clocks over a longer time period.

In practice, the same time drift can be observed by an application across multiple navigations: the application can record the logical time in each context and use a client or server time synchronization mechanism to infer changes in the user's clock. Similarly, lower-layer mechanisms such as TCP timestamps may reveal the same high-resolution information to the server without the need for multiple visits. As such, the information provided by this API should not expose any significant or previously unavailable entropy about the user.

The current definition of [time origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-time-origin) for a [`Document`](https://dom.spec.whatwg.org/#document) exposes the total time of cross-origin redirects prior to the request arriving at the document's origin. This exposes cross-origin information, however it's not yet decided how to mitigate this without causing major breakages to performance metrics.

To track the discussion, refer to [Navigation Timing Issue 160](https://github.com/w3c/navigation-timing/issues/160).

As well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative.

The key words _MUST_ and _SHOULD_ in this document are to be interpreted as described in [BCP 14](https://datatracker.ietf.org/doc/html/bcp14) \[[RFC2119](https://w3c.github.io/hr-time/#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://w3c.github.io/hr-time/#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

Some conformance requirements are phrased as requirements on attributes, methods or objects. Such requirements are to be interpreted as requirements on user agents.

-   [clock](https://w3c.github.io/hr-time/#dfn-clock)
-   [coarsen time](https://w3c.github.io/hr-time/#dfn-coarsen-time)
-   [coarsened moments](https://w3c.github.io/hr-time/#dfn-moment)
-   [coarsened shared current time](https://w3c.github.io/hr-time/#dfn-coarsened-shared-current-time)
-   [current high resolution time](https://w3c.github.io/hr-time/#dfn-current-high-resolution-time)
-   [current monotonic time](https://w3c.github.io/hr-time/#dfn-current-monotonic-time)
-   [current relative timestamp](https://w3c.github.io/hr-time/#dfn-current-relative-timestamp)
-   current wall time
    -   [definition of](https://w3c.github.io/hr-time/#dfn-current-wall-time)
    -   [definition of](https://w3c.github.io/hr-time/#dfn-eso-current-wall-time)
-   [`DOMHighResTimeStamp`](https://w3c.github.io/hr-time/#dom-domhighrestimestamp)
-   [duration](https://w3c.github.io/hr-time/#dfn-duration)
-   [duration from](https://w3c.github.io/hr-time/#dfn-duration-from)
-   [`EpochTimeStamp`](https://w3c.github.io/hr-time/#dom-epochtimestamp)
-   [estimated monotonic time of the Unix epoch](https://w3c.github.io/hr-time/#dfn-estimated-monotonic-time-of-the-unix-epoch)
-   [get time origin timestamp](https://w3c.github.io/hr-time/#dfn-get-time-origin-timestamp)
-   [implicitly convert a duration to a timestamp](https://w3c.github.io/hr-time/#dfn-implicitly-convert-a-duration-to-a-timestamp)
-   [monotonic clock](https://w3c.github.io/hr-time/#dfn-monotonic-clock)
-   [`now()`](https://w3c.github.io/hr-time/#dom-performance-now) method for `Performance`
-   [`performance`](https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance) attribute for `WindowOrWorkerGlobalScope`
-   [`Performance`](https://w3c.github.io/hr-time/#dom-performance) interface
-   [relative high resolution coarse time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-coarse-time)
-   [relative high resolution time](https://w3c.github.io/hr-time/#dfn-relative-high-resolution-time)
-   [`timeOrigin`](https://w3c.github.io/hr-time/#dom-performance-timeorigin) attribute for `Performance`
-   [`toJSON()`](https://w3c.github.io/hr-time/#dom-performance-tojson) method for `Performance`
-   [Unix epoch](https://w3c.github.io/hr-time/#dfn-unix-epoch)
-   unsafe current time
    -   [definition of](https://w3c.github.io/hr-time/#dfn-unsafe-current-time)
    -   [definition of](https://w3c.github.io/hr-time/#wall-clock-unsafe-current-time)
    -   [definition of](https://w3c.github.io/hr-time/#monotonic-clock-unsafe-current-time)
-   [unsafe moment](https://w3c.github.io/hr-time/#dfn-unsafe-moment)
-   [unsafe shared current time](https://w3c.github.io/hr-time/#dfn-unsafe-shared-current-time)
-   [wall clock](https://w3c.github.io/hr-time/#dfn-wall-clock)

-   \[[DOM](https://w3c.github.io/hr-time/#bib-dom)\] defines the following:
    -   `Document` interface
    -   `EventTarget` interface
    -   `timeStamp` attribute (for `Event`)
-   \[[ECMA-262](https://w3c.github.io/hr-time/#bib-ecma-262)\] defines the following:
    -   Date
    -   Date.now()
    -   time
-   \[[HTML](https://w3c.github.io/hr-time/#bib-html)\] defines the following:
    -   `BroadcastChannel` interface
    -   cross-origin isolated capability (for environment settings object)
    -   environment settings object
    -   familiar with
    -   global object
    -   global object (for `realm`)
    -   navigate
    -   parse a duration string
    -   `postMessage(message, options)` (for `Window`)
    -   relevant global object
    -   relevant settings object
    -   run a worker
    -   `SharedWorker` interface
    -   time origins (for environment settings object)
    -   `Window` interface
    -   `WindowOrWorkerGlobalScope` interface
    -   `Worker` interface
-   \[[INFRA](https://w3c.github.io/hr-time/#bib-infra)\] defines the following:
    -   implementation-defined
    -   tracking vector
    -   user agent
-   \[[REPORTING](https://w3c.github.io/hr-time/#bib-reporting)\] defines the following:
    -   generation time
-   \[[SERVICE-WORKERS](https://w3c.github.io/hr-time/#bib-service-workers)\] defines the following:
    -   `ServiceWorker` interface
-   \[[TEMPORAL](https://w3c.github.io/hr-time/#bib-temporal)\] defines the following:
    -   Temporal.Instant
-   \[[WEBIDL](https://w3c.github.io/hr-time/#bib-webidl)\] defines the following:
    -   `[Default]` extended attribute
    -   default toJSON steps
    -   `double` type
    -   `[Exposed]` extended attribute
    -   `object` type
    -   `[Replaceable]` extended attribute
    -   this
    -   `unsigned long long` type

```
<span data-idl="" data-title="DOMHighResTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-double" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-double" id="ref-for-index-term-double-type-3">double<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-13"><code>DOMHighResTimeStamp<!---0.176915%--></code></a>;<!---0.176915%--></span>

<span data-idl="" data-title="EpochTimeStamp">typedef<span> <a data-link-type="idl" data-xref-type="_IDL_" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-unsigned-long-long" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-unsigned-long-long" id="ref-for-index-term-unsigned-long-long-type-2">unsigned long long<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="" data-link-type="typedef" href="https://w3c.github.io/hr-time/#dom-epochtimestamp" id="ref-for-dom-epochtimestamp-4"><code>EpochTimeStamp<!---0.176915%--></code></a>;<!---0.176915%--></span>

<span data-idl="" data-title="Performance">[<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Exposed" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Exposed" id="ref-for-index-term-exposed-extended-attribute-2">Exposed<!---0.176915%--></a>=(Window,Worker)<!---0.176915%--></span>]
interface <a data-link-for="" data-link-type="interface" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-9"><code>Performance<!---0.176915%--></code></a> : <span><a data-link-type="idl" data-xref-type="_IDL_" data-cite="dom" data-cite-path="/" data-cite-frag="eventtarget" data-type="interface" href="https://dom.spec.whatwg.org/#eventtarget" id="ref-for-index-term-eventtarget-interface-2">EventTarget<!---0.176915%--></a><!---0.176915%--></span> {<span data-idl="" data-title="now" data-dfn-for="Performance"><span>
    <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-14"><code>DOMHighResTimeStamp<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-now" id="ref-for-dom-performance-now-6"><code>now<!---0.176915%--></code></a>();<!---0.176915%--></span><span data-idl="" data-title="timeOrigin" data-dfn-for="Performance">
    readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-domhighrestimestamp" id="ref-for-dom-domhighrestimestamp-15"><code>DOMHighResTimeStamp<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-performance-timeorigin" id="ref-for-dom-performance-timeorigin-6"><code>timeOrigin<!---0.176915%--></code></a>;<!---0.176915%--></span><span data-idl="" data-title="toJSON" data-dfn-for="Performance">
    [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Default" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Default" id="ref-for-index-term-default-extended-attribute-2">Default<!---0.176915%--></a><!---0.176915%--></span>]<span> <a data-link-type="interface" data-xref-type="interface" data-cite="webidl" data-cite-path="/" data-cite-frag="idl-object" data-type="interface" href="https://webidl.spec.whatwg.org/#idl-object" id="ref-for-index-term-object-type-2">object<!---0.176915%--></a><!---0.176915%--></span> <a data-link-for="Performance" data-link-type="method" href="https://w3c.github.io/hr-time/#dom-performance-tojson" id="ref-for-dom-performance-tojson-2"><code>toJSON<!---0.176915%--></code></a>();<!---0.176915%--></span>
};<!---0.176915%--></span>

<span data-idl="" data-title="WindowOrWorkerGlobalScope">partial interface mixin <a data-idl="partial" data-link-type="interface" data-title="WindowOrWorkerGlobalScope" data-xref-type="interface" data-dfn-for="WindowOrWorkerGlobalScope" data-cite="html" data-cite-path="/webappapis.html" data-cite-frag="windoworworkerglobalscope" data-type="interface" href="https://html.spec.whatwg.org/multipage/webappapis.html#windoworworkerglobalscope" id="ref-for-index-term-windoworworkerglobalscope-interface-3">WindowOrWorkerGlobalScope<!---0.176915%--></a> {<span data-idl="" data-title="performance" data-dfn-for="WindowOrWorkerGlobalScope">
  [<span><a data-xref-type="extended-attribute" data-cite="webidl" data-cite-path="/" data-cite-frag="Replaceable" data-type="extended-attribute" href="https://webidl.spec.whatwg.org/#Replaceable" id="ref-for-index-term-replaceable-extended-attribute-2">Replaceable<!---0.176915%--></a><!---0.176915%--></span>] readonly attribute<span> <a data-link-type="idl" data-xref-type="_IDL_" href="https://w3c.github.io/hr-time/#dom-performance" id="ref-for-dom-performance-10"><code>Performance<!---0.176915%--></code></a><!---0.176915%--></span> <a data-link-for="WindowOrWorkerGlobalScope" data-link-type="attribute" href="https://w3c.github.io/hr-time/#dom-windoworworkerglobalscope-performance" id="ref-for-dom-windoworworkerglobalscope-performance-2"><code>performance<!---0.176915%--></code></a>;<!---0.176915%--></span>
};<!---0.176915%--></span>
```

Thanks to Arvind Jain, Angelos D. Keromytis, Boris Zbarsky, Jason Weber, Karen Anderson, Nat Duca, Philippe Le Hegaret, Ryosuke Niwa, Simha Sethumadhavan, Todd Reifsteck, Tony Gentilcore, Vasileios P. Kemerlis, Yoav Weiss, and Yossef Oren for their contributions to this work.

\[dom\]

[DOM Standard](https://dom.spec.whatwg.org/). Anne van Kesteren. WHATWG. Living Standard. URL: [https://dom.spec.whatwg.org/](https://dom.spec.whatwg.org/)

\[ECMA-262\]

[ECMAScript Language Specification](https://tc39.es/ecma262/multipage/). Ecma International. URL: [https://tc39.es/ecma262/multipage/](https://tc39.es/ecma262/multipage/)

\[html\]

[HTML Standard](https://html.spec.whatwg.org/multipage/). Anne van Kesteren; Domenic Denicola; Ian Hickson; Philip Jägenstedt; Simon Pieters. WHATWG. Living Standard. URL: [https://html.spec.whatwg.org/multipage/](https://html.spec.whatwg.org/multipage/)

\[infra\]

[Infra Standard](https://infra.spec.whatwg.org/). Anne van Kesteren; Domenic Denicola. WHATWG. Living Standard. URL: [https://infra.spec.whatwg.org/](https://infra.spec.whatwg.org/)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[SPECTRE\]

[Spectre Attacks: Exploiting Speculative Execution](https://spectreattack.com/spectre.pdf). Paul Kocher; Jann Horn; Anders Fogh; Daniel Genkin; Daniel Gruss; Werner Haas; Mike Hamburg; Moritz Lipp; Stefan Mangard; Thomas Prescher; Michael Schwarz; Yuval Yarom. January 2018. URL: [https://spectreattack.com/spectre.pdf](https://spectreattack.com/spectre.pdf)

\[Temporal\]

[Temporal](https://tc39.es/proposal-temporal/). ECMA TC39. Stage 3 Proposal. URL: [https://tc39.es/proposal-temporal/](https://tc39.es/proposal-temporal/)

\[WEBIDL\]

[Web IDL Standard](https://webidl.spec.whatwg.org/). Edgar Chen; Timothy Gu. WHATWG. Living Standard. URL: [https://webidl.spec.whatwg.org/](https://webidl.spec.whatwg.org/)

\[CACHE-ATTACKS\]

[The Spy in the Sandbox - Practical Cache Attacks in Javascript](https://arxiv.org/abs/1502.07373). Yossef Oren; Vasileios P. Kemerlis; Simha Sethumadhavan; Angelos D. Keromytis. 1 March 2015. URL: [https://arxiv.org/abs/1502.07373](https://arxiv.org/abs/1502.07373)

\[reporting\]

[Reporting API](https://www.w3.org/TR/reporting-1/). Douglas Creager; Ian Clelland; Mike West. W3C. 13 August 2024. W3C Working Draft. URL: [https://www.w3.org/TR/reporting-1/](https://www.w3.org/TR/reporting-1/)

\[service-workers\]

[Service Workers](https://www.w3.org/TR/service-workers/). Jake Archibald; Marijn Kruisselbrink. W3C. 12 July 2022. W3C Candidate Recommendation. URL: [https://www.w3.org/TR/service-workers/](https://www.w3.org/TR/service-workers/)
org/). Anne van Kesteren. WHATWG. Living Standard. URL: [https://dom.spec.whatwg.org/](https://dom.spec.whatwg.org/)

\[ECMA-262\]

[ECMAScript Language Specification](https://tc39.es/ecma262/multipage/). Ecma International. URL: [https://tc39.es/ecma262/multipage/](https://tc39.es/ecma262/multipage/)

\[html\]

[HTML Standard](https://html.spec.whatwg.org/multipage/). Anne van Kesteren; Domenic Denicola; Ian Hickson; Philip Jägenstedt; Simon Pieters. WHATWG. Living Standard. URL: [https://html.spec.whatwg.org/multipage/](https://html.spec.whatwg.org/multipage/)

\[infra\]

[Infra Standard](https://infra.spec.whatwg.org/). Anne van Kesteren; Domenic Denicola. WHATWG. Living Standard. URL: [https://infra.spec.whatwg.org/](https://infra.spec.whatwg.org/)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[SPECTRE\]

[Spectre Attacks: Exploiting Speculative Execution](https://spectreattack.com/spectre.pdf). Paul Kocher; Jann Horn; Anders Fogh; Daniel Genkin; Daniel Gruss; Werner Haas; Mike Hamburg; Moritz Lipp; Stefan Mangard; Thomas Prescher; Michael Schwarz; Yuval Yarom. January 2018. URL: [https://spectreattack.com/spectre.pdf](https://spectreattack.com/spectre.pdf)

\[Temporal\]

[Temporal](https://tc39.es/proposal-temporal/). ECMA TC39. Stage 3 Proposal. URL: [https://tc39.es/proposal-temporal/](https://tc39.es/proposal-temporal/)

\[WEBIDL\]

[Web IDL Standard](https://webidl.spec.whatwg.org/). Edgar Chen; Timothy Gu. WHATWG. Living Standard. URL: [https://webidl.spec.whatwg.org/](https://webidl.spec.whatwg.org/)

\[CACHE-ATTACKS\]

[The Spy in the Sandbox - Practical Cache Attacks in Javascript](https://arxiv.org/abs/1502.07373). Yossef Oren; Vasileios P. Kemerlis; Simha Sethumadhavan; Angelos D. Keromytis. 1 March 2015. URL: [https://arxiv.org/abs/1502.07373](https://arxiv.org/abs/1502.07373)

\[reporting\]

[Reporting API](https://www.w3.org/TR/reporting-1/). Douglas Creager; Ian Clelland; Mike West. W3C. 9 August 2024. W3C Working Draft. URL: [https://www.w3.org/TR/reporting-1/](https://www.w3.org/TR/reporting-1/)

\[service-workers\]

[Service Workers](https://www.w3.org/TR/service-workers/). Jake Archibald; Marijn Kruisselbrink. W3C. 12 July 2022. W3C Candidate Recommendation. URL: [https://www.w3.org/TR/service-workers/](https://www.w3.org/TR/service-workers/)
