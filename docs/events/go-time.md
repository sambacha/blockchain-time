---
created: 2022-06-17T10:48:31 (UTC -07:00)
tags: []
source: https://topic.alibabacloud.com/a/in-depth-understanding-of-go-time-processing-time_1_38_30918531.html
author: 
---

# In-depth understanding of Go time processing. Time)

1. Preface
Time includes time values and time zones, and there are incomplete and ambiguous times when you do not include timezone information. When transmitting or

This is a creation in Article, where the information may have evolved or changed.

1\. Preface

Time includes time values and time zones, and there are incomplete and ambiguous times when you do not include timezone information. When transmitting or parsing time data, you should use a format that has no time zone ambiguity, like the HTTP protocol or UNIX-TIMESTAMP, if you use some non-standard time representation format (such as Yyyy-mm-dd HH:MM:SS) that does not contain a time zone, it is a hidden danger. Because the default settings for the scene are used for parsing, such as the system time zone, the database default time zone can cause an incident. Ensure that server systems, databases, applications use a unified time zone, and if the application maintains a different time zone for some historical reasons, carefully examine the code when programming and know the behavior of time data when it is exchanged between programs that use different time zones. The third section explains in detail the Go program's time in different scenarios. The behavior of time.

2\. Data structure of time

Before go1.9, time. Time is defined as

```golang
type Time struct {
// sec gives the number of seconds elapsed since
// January 1, year 1 00:00:00 UTC.
sec int64
// nsec specifies a non-negative nanosecond
// offset within the second named by Seconds.
// It must be in the range [0, 999999999].
nsec int32
// loc specifies the Location that should be used to
// determine the minute, hour, month, day, and year
// that correspond to this Time.
// The nil location means UTC.
// All UTC times are represented with loc==nil, never loc==&utcLoc.
loc *Location
}


```

The SEC represents the number of seconds from January 1, 1 A.D. 00:00:00UTC to the number of integers to represent, nsec represents the remaining nanoseconds, and Loc represents the time zone. The SEC and nsec handle the time value without ambiguity, and Loc handles the offset.

Because 2017 leap one second, the International clock adjustment, go program two times take Time.now () subtract the time difference has been unexpectedly negative, resulting in CloudFlare CDN service interruption, see https://blog.cloudflare.com/ how-and-why-the-leap-second-affected-cloudflare-dns/, go1.9 modifies the implementation of Time.time without affecting existing application code. The time.time of go1.9 is defined as

```golang
// A Time represents an instant in time with nanosecond precision.
//
// Programs using times should typically store and pass them as values,
// not pointers. That is, time variables and struct fields should be of
// type time.Time, not *time.Time.
//
// A Time value can be used by multiple goroutines simultaneously except
// that the methods GobDecode, UnmarshalBinary, UnmarshalJSON and
// UnmarshalText are not concurrency-safe.
//
// Time instants can be compared using the Before, After, and Equal methods.
// The Sub method subtracts two instants, producing a Duration.
// The Add method adds a Time and a Duration, producing a Time.
//
// The zero value of type Time is January 1, year 1, 00:00:00.000000000 UTC.
// As this time is unlikely to come up in practice, the IsZero method gives
// a simple way of detecting a time that has not been initialized explicitly.
//
// Each Time has associated with it a Location, consulted when computing the
// presentation form of the time, such as in the Format, Hour, and Year methods.
// The methods Local, UTC, and In return a Time with a specific location.
// Changing the location in this way changes only the presentation; it does not
// change the instant in time being denoted and therefore does not affect the
// computations described in earlier paragraphs.
//
// Note that the Go == operator compares not just the time instant but also the
// Location and the monotonic clock reading. Therefore, Time values should not
// be used as map or database keys without first guaranteeing that the
// identical Location has been set for all values, which can be achieved
// through use of the UTC or Local method, and that the monotonic clock reading
// has been stripped by setting t = t.Round(0). In general, prefer t.Equal(u)
// to t == u, since t.Equal uses the most accurate comparison available and
// correctly handles the case when only one of its arguments has a monotonic
// clock reading.
//
// In addition to the required “wall clock” reading, a Time may contain an optional
// reading of the current process's monotonic clock, to provide additional precision
// for comparison or subtraction.
// See the “Monotonic Clocks” section in the package documentation for details.
//
type Time struct {
// wall and ext encode the wall time seconds, wall time nanoseconds,
// and optional monotonic clock reading in nanoseconds.
//
// From high to low bit position, wall encodes a 1-bit flag (hasMonotonic),
// a 33-bit seconds field, and a 30-bit wall time nanoseconds field.
// The nanoseconds field is in the range [0, 999999999].
// If the hasMonotonic bit is 0, then the 33-bit field must be zero
// and the full signed 64-bit wall seconds since Jan 1 year 1 is stored in ext.
// If the hasMonotonic bit is 1, then the 33-bit field holds a 33-bit
// unsigned wall seconds since Jan 1 year 1885, and ext holds a
// signed 64-bit monotonic clock reading, nanoseconds since process start.
wall uint64
ext  int64
// loc specifies the Location that should be used to
// determine the minute, hour, month, day, and year
// that correspond to this Time.
// The nil location means UTC.
// All UTC times are represented with loc==nil, never loc==&utcLoc.
loc *Location
}

```

3\. The behavior of Time

1.  Construction time-Gets the current time-time. Now (), time. Now () Use local time. local time zone, depending on the operating system environment settings, take precedence to "TZ" this environment variable, and then take/etc/localtime, will not be taken in UTC backstop.
    
    ```golang
    func Now() Time {
    sec, nsec := now()
    return Time{sec + unixToInternal, nsec, Local}
    }
    ```
    

1.  Construction time-Gets the current time-time for a time zone. Now (). In (), the method of theIn()time struct sets only Loc, and does not change the value of the Times. In particular, if you are getting the current UTC time, you can use Time.now (). UTC ().  
    The time zone cannot be nil. There are only two time-zone variables in the package. Local and TIME.UTC. The other time zone variables are obtained in two ways, one is through the. The Loadlocation function is loaded according to the time zone name, the time zone name is found in the IANA timezone database, Loadlocation first finds the system zoneinfo, and then looks for it$GOROOT/lib/time/zoneinfo.zip. The other is called directly when the time zone name and offset are knowntime.FixedZone("$zonename", $offsetSecond)constructs a Location object.
    
    ```golang
    // In returns t with the location information set to loc.
    //
    // In panics if loc is nil.
    func (t Time) In(loc *Location) Time {
    if loc == nil {
    panic("time: missing Location in call to Time.In")
    }
    t.setLoc(loc)
    return t
    }
    // LoadLocation returns the Location with the given name.
    //
    // If the name is "" or "UTC", LoadLocation returns UTC.
    // If the name is "Local", LoadLocation returns Local.
    //
    // Otherwise, the name is taken to be a location name corresponding to a file
    // in the IANA Time Zone database, such as "America/New_York".
    //
    // The time zone database needed by LoadLocation may not be
    // present on all systems, especially non-Unix systems.
    // LoadLocation looks in the directory or uncompressed zip file
    // named by the ZONEINFO environment variable, if any, then looks in
    // known installation locations on Unix systems,
    // and finally looks in $GOROOT/lib/time/zoneinfo.zip.
    func LoadLocation(name string) (*Location, error) {
    if name == "" || name == "UTC" {
    return UTC, nil
    }
    if name == "Local" {
    return Local, nil
    }
    if zoneinfo != "" {
    if z, err := loadZoneFile(zoneinfo, name); err == nil {
    z.name = name
    return z, nil
    }
    }
    return loadLocation(name)
    }
    
    ```
    

1.  Construction Time-Manual construction time-time. Date (), passing in the year Yuanri when the second nanosecond and time zone variable location constructs a time. The time to specify location is obtained.
    
    ```golang
    func Date(year int, month Month, day, hour, min, sec, nsec int, loc *Location) Time {
    if loc == nil {
    panic("time: missing Location in call to Date")
    }
    .....
    }
    
    

2.  Construction time-constructs the time from the Unix timestamp. Unix (), incoming seconds and nanosecond constructs.
3.  Serialization of deserialization time-text and JSON, FMT. Sprintf,fmt. SSCANF, JSON. Marshal, JSON. Unmarshal, the time format used includes the time zone information, serialization using Rfc3339nano () "2006-01-02t15:04:05.999999999z07:00", deserialization using RFC3339 () " 2006-01-02t15:04:05z07:00 ", deserialization does not have a nanosecond value and can be serialized successfully.
    
    ```golang
    // String returns the time formatted using the format string
    //"2006-01-02 15:04:05.999999999 -0700 MST"
    func (t Time) String() string {
    return t.Format("2006-01-02 15:04:05.999999999 -0700 MST")
    }
    // MarshalJSON implements the json.Marshaler interface.
    // The time is a quoted string in RFC 3339 format, with sub-second precision added if present.
    func (t Time) MarshalJSON() ([]byte, error) {
    if y := t.Year(); y < 0 || y >= 10000 {
    // RFC 3339 is clear that years are 4 digits exactly.
    // See golang.org/issue/4556#c15 for more discussion.
    return nil, errors.New("Time.MarshalJSON: year outside of range [0,9999]")
    }
    b := make([]byte, 0, len(RFC3339Nano)+2)
    b = append(b, '"')
    b = t.AppendFormat(b, RFC3339Nano)
    b = append(b, '"')
    return b, nil
    }
    // UnmarshalJSON implements the json.Unmarshaler interface.
    // The time is expected to be a quoted string in RFC 3339 format.
    func (t *Time) UnmarshalJSON(data []byte) error {
    // Ignore null, like in the main JSON package.
    if string(data) == "null" {
    return nil
    }
    // Fractional seconds are handled implicitly by Parse.
    var err error
    *t, err = Parse(`"`+RFC3339+`"`, string(data))
    return err
    }
    
    ```
    

1.  Serialization deserialization time date in-http protocol, unified GMT, code in net/http/server.go:878
    
    ```golang
    // TimeFormat is the time format to use when generating times in HTTP
    // headers. It is like time.RFC1123 but hard-codes GMT as the time
    // zone. The time being formatted must be in UTC for Format to
    // generate the correct format.
    //
    // For parsing this time format, see ParseTime.
    const TimeFormat = "Mon, 02 Jan 2006 15:04:05 GMT"
    
    ```
    

1.  Serialization deserialization time-time.Format("$layout"),time.Parse("$layout","$value")time.ParseInLocation("$layout","$value","$Location")
    
    -   time.Format("$layout")When you format a time, the time zone participates in the calculation. Adjust the time. TIME's Year () month () date (), and so on, will participate in the calculation, get a correct time string with offset correction, and if$layoutthe time zone is specified, the time zone information will be reflected in the formatted string. If$layoutNo display time zone is specified, then the string is only time-free, the timezone is implied, time. Time-zone in an object.
    
    -   time.Parse("$layout","$value"), if$layoutyou specify a time zone, the time zone information will be reflected in the format. The time object. **If you$layoutdo not specify a display time zone, the use considers this to be a UTC time and the time zone is UTC.**
    -   time.ParseInLocation("$layout","$value","$Location")Using the time zone resolution of the parameter, it is recommended to use this, no ambiguity.
        
        ```golang
        // Parse parses a formatted string and returns the time value it represents.
        // The layout  defines the format by showing how the reference time,
        // defined to be
        //Mon Jan 2 15:04:05 -0700 MST 2006
        // would be interpreted if it were the value; it serves as an example of
        // the input format. The same interpretation will then be made to the
        // input string.
        //
        // Predefined layouts ANSIC, UnixDate, RFC3339 and others describe standard
        // and convenient representations of the reference time. For more information
        // about the formats and the definition of the reference time, see the
        // documentation for ANSIC and the other constants defined by this package.
        // Also, the executable example for time.Format demonstrates the working
        // of the layout string in detail and is a good reference.
        //
        // Elements omitted from the value are assumed to be zero or, when
        // zero is impossible, one, so parsing "3:04pm" returns the time
        // corresponding to Jan 1, year 0, 15:04:00 UTC (note that because the year is
        // 0, this time is before the zero Time).
        // Years must be in the range 0000..9999. The day of the week is checked
        // for syntax but it is otherwise ignored.
        //
        // In the absence of a time zone indicator, Parse returns a time in UTC.
        //
        // When parsing a time with a zone offset like -0700, if the offset corresponds
        // to a time zone used by the current location (Local), then Parse uses that
        // location and zone in the returned time. Otherwise it records the time as
        // being in a fabricated location with time fixed at the given zone offset.
        //
        // No checking is done that the day of the month is within the month's
        // valid dates; any one- or two-digit value is accepted. For example
        // February 31 and even February 99 are valid dates, specifying dates
        // in March and May. This behavior is consistent with time.Date.
        //
        // When parsing a time with a zone abbreviation like MST, if the zone abbreviation
        // has a defined offset in the current location, then that offset is used.
        // The zone abbreviation "UTC" is recognized as UTC regardless of location.
        // If the zone abbreviation is unknown, Parse records the time as being
        // in a fabricated location with the given zone abbreviation and a zero offset.
        // This choice means that such a time can be parsed and reformatted with the
        // same layout losslessly, but the exact instant used in the representation will
        // differ by the actual zone offset. To avoid such problems, prefer time layouts
        // that use a numeric zone offset, or use ParseInLocation.
        func Parse(layout, value string) (Time, error) {
        return parse(layout, value, UTC, Local)
        }
        // ParseInLocation is like Parse but differs in two important ways.
        // First, in the absence of time zone information, Parse interprets a time as UTC;
        // ParseInLocation interprets the time as in the given location.
        // Second, when given a zone offset or abbreviation, Parse tries to match it
        // against the Local location; ParseInLocation uses the given location.
        func ParseInLocation(layout, value string, loc *Location) (Time, error) {
        return parse(layout, value, loc, loc)
        }
        func parse(layout, value string, defaultLocation, local *Location) (Time, error) {
        .....
        }
       
        
2.  Serializes the time processing in the deserialization time-go-sql-driver/mysql.  
    MySQL driver parsing time is the premise of the connection string plus parsetime and loc, if Parsetime is false, will be the date type of MySQL \[\]byte/string self-processing, parsetime to true processing time, LOC Specifies the time zone in MySQL where data is stored, if LOC is not specified, in UTC. Both serialization and deserialization use the Set loc in the connection string, and the time zone information for the parameters of the Time.time type in the SQL statement, if different from Loc, calls the method to thet.In(loc)time zone.
    
    -   The code that parses the connection string is located in the Parsedsnparams function https://github.com/go-sql-driver/mysql/blob/master/dsn.go#L467-L490
        
        ```golang
        // Time Location
        case "loc":
        if value, err = url.QueryUnescape(value); err != nil {
        return
        }
        cfg.Loc, err = time.LoadLocation(value)
        if err != nil {
        return
        }
        // time.Time parsing
        case "parseTime":
        var isBool bool
        cfg.ParseTime, isBool = readBool(value)
        if !isBool {
        return errors.New("invalid bool value: " + value)
        }
        
        ```
        
    -   The code that resolves the parameters of the Time.time type in the SQL statement is located in the Mysqlconn.interpolateparams method https://github.com/go-sql-driver/mysql/blob/master/ connection.go#l230-l273
        
        ```golang
        case time.Time:
        if v.IsZero() {
        buf = append(buf, "'0000-00-00'"...)
        } else {
        v := v.In(mc.cfg.Loc)
        v = v.Add(time.Nanosecond * 500) // To round under microsecond
        year := v.Year()
        year100 := year / 100
        year1 := year % 100
        month := v.Month()
        day := v.Day()
        hour := v.Hour()
        minute := v.Minute()
        second := v.Second()
        micro := v.Nanosecond() / 1000
        
        buf = append(buf, []byte{
        '\'',
        digits10[year100], digits01[year100],
        digits10[year1], digits01[year1],
        '-',
        digits10[month], digits01[month],
        '-',
        digits10[day], digits01[day],
        ' ',
        digits10[hour], digits01[hour],
        ':',
        digits10[minute], digits01[minute],
        ':',
        digits10[second], digits01[second],
        }...)
        
        if micro != 0 {
        micro10000 := micro / 10000
        micro100 := micro / 100 % 100
        micro1 := micro % 100
        buf = append(buf, []byte{
        '.',
        digits10[micro10000], digits01[micro10000],
        digits10[micro100], digits01[micro100],
        digits10[micro1], digits01[micro1],
        }...)
        }
        buf = append(buf, '\'')
        }
        
        
        ```
        
    
    -   The code to parse the time from the MySQL data stream is located in the Textrows.readrow method https://github.com/go-sql-driver/mysql/blob/master/packets.go#L772-L777, **Note that whenever the MySQL connection string is set to Parsetime=true, the time is resolved, whether you are using string or timing. Time is received.**
        
        ```golang
        case time.Time:
        if v.IsZero() {
        buf = append(buf, "'0000-00-00'"...)
        } else {
        v := v.In(mc.cfg.Loc)
        v = v.Add(time.Nanosecond * 500) // To round under microsecond
        year := v.Year()
        year100 := year / 100
        year1 := year % 100
        month := v.Month()
        day := v.Day()
        hour := v.Hour()
        minute := v.Minute()
        second := v.Second()
        micro := v.Nanosecond() / 1000
        
        buf = append(buf, []byte{
        '\'',
        digits10[year100], digits01[year100],
        digits10[year1], digits01[year1],
        '-',
        digits10[month], digits01[month],
        '-',
        digits10[day], digits01[day],
        ' ',
        digits10[hour], digits01[hour],
        ':',
        digits10[minute], digits01[minute],
        ':',
        digits10[second], digits01[second],
        }...)
        
        if micro != 0 {
        micro10000 := micro / 10000
        micro100 := micro / 100 % 100
        micro1 := micro % 100
        buf = append(buf, []byte{
        '.',
        digits10[micro10000], digits01[micro10000],
        digits10[micro100], digits01[micro100],
        digits10[micro1], digits01[micro1],
        }...)
        }
        buf = append(buf, '\'')
        }
        
        ```
        

4\. Time zone handling inappropriate cases

2.  A service frequently uses the latest exchange rate, so the latest exchange rate object is cached, the exchange rate object expires at 0 o'clock GMT, the exchange rate expires from the database to the latest exchange rate, set the expiration time code as follows:
    
        ```golang
    var startTime string = time.Now().UTC().Add(8 * time.Hour).Format("2006-01-02")
    tm2, _ := time.Parse("2006-01-02", startTime)
    lastTime = tm2.Unix() + 24*60*60
    
    ```
    
    This code uses time. Parse, if the time format is not specified, then the second day of the local time zone is used 0 o'clock, the server time zone is set to UTC0, and the exchange rate cache is updated at UTC 0 at GMT eight o'clock.
    
3.  There is a getbjtime () method in the public library, and the comment says to convert the server UTC to Beijing time, the code is as follows
    
        ```golang
    // original
    func GetBjTime () time.Time {
    // Convert server UTC to Beijing time
    uTime: = time.Now (). UTC ()
    dur, _: = time.ParseDuration ("+ 8h")
    return uTime.Add (dur)
    }
    // change
    func GetBjTime () time.Time {
    // Convert server UTC to Beijing time
    uTime: = time.Now ()
    return uTime.In (time.FixedZone ("CST", 8 * 60 * 60))
    }
    ```
    
    The
    
    colleague uses this method to get the time. Time participates in the calculation and finds 8 more hours. Feel that there is a problem, colleagues and I discussed, we come to the conclusion of the effect of the original function directly changed, we do not realize that this is a very dangerous operation, only so the danger is because this function has been used in many service code (to stabilize!). Do not tamper with the public library!!!). This function was previously used because the old Java project was running on a system with a time zone of East eight, and a lot of code used the East eight time, but the database MySQL time zone was set to UTC, and the Go Project was also running in the UTC time zone. That is, the Java project in the time zone is the UTC database as the East Eight, Java program to MySQL to write the time string East Eight, while the sequel software to see the table content while the string is the same, but in fact, the internal UTC time, The LOC option in the Go code's MySQL connection string is empty, and the UTC time zone is used to parse the data, and the data gets eight hours more. For example, Java code to the MySQL insert a "2017-10-29 22:00:00" data originally intended to be East eight October 29, 2017 22 o'clock, but in the internal MySQL view, this is UTC October 29, 2017 22 o'clock, Convert to East Eight the time is October 30, 2017 6 o'clock, if other program resolves to think Time data is the UTC time zone of MySQL, then will get an error time. That's whytime is used to write data to the table that the Java code creates in go. Now (). UTC (). ADD (time. HOUR\*8)directly add eight hours to make the Java project behave the same, take UTC's data in the East eight zone time.
    
    After thinking, in the case of this database sometimes inconsistent data, in the absence of a unified UTC time zone, you should use the MySQL time string instead of time.time to avoid time zone implicit conversion problems, write-in arguments to string type of time string, Parse the time string first, and then determine when the table is built using the east eight time string or UTC time string time.parseinlocation to get the time object, MySQL connection string parsetime option to set to false. For example, I want to save the current time in the eight zone in MySQL, the SQL parameter uses the format string instead of the Time.time, and the originaltime.Now().UTC().Add(time.Hour\*8).Format("2006-01-02 15:04:05")and modifiedtime.Now().In(time.FixedZone("CST", 8\*60\*60))output will be the same, but the latter is the correct time for the East eight zone. Original Getbjtime () Returns time. Time may return a string with getbeijingnowtimestring to better reflect the meaning.
    

5\. Time-related standards

-   UTC
    
    > Reconcile the World (English: Coordinated Universal time, French: Temps universel Coordonné, or UTC) are the most important worlds Standard, which is based on atomic time-of-second length and is as close to Greenwich Mean time as possible at all times. The Republic of China adopts the CNS 7648 data element and interchange Format – Information exchange – representation of date and time (similar to ISO 8601) as world coordination time. The People's Republic of China adopts ISO 8,601:2000 national standard GB/T 7408-2005 "data element and interchange Format information interchange date and time notation" also known as coordinated World time. The  
    > Coordinated Universal Time is the world's primary clock and time standard for adjusting clocks and times, and it is not more than 1 seconds \[4\] when compared to the 0-degree longitude of the sun, and does not observe daylight savings. Coordinated world time is one of several alternative time systems closest to Greenwich Mean Time (GMT). For most purposes, UTC time is considered to be interchangeable with GMT time, but GMT is no longer determined by the scientific community.
    
-   ISO 8601 calculates the day of the week/cycle time of the year rrlue/will use this standard
    
    > International Standard ISO 8601, is the date of the International Organization for Standardization And the representation of time in the form of data storage and exchange, information exchange, representation of date and time. Currently the third edition of "iso8601:2004" replaces the first version of "iso8601:1988" with the second edition "iso8601:2000".
    
-   Unix time
    
    > Unix time, or POSIX time, is the time representation used by UNIX or Unix-like systems: From coordinated GMT January 1, 1970 0:0 0 seconds to now In the total number of seconds, regardless of leap seconds \[1\]. Unix time on most UNIX systems can be checked by the date +%s directive.
    
-   time zone
    
    > Time zone list
