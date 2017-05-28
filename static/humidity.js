// August-Roche-Magnus approximation constants
var c1 = 17.625;
var c2 = 243.04;

function compute_dew(rh, temp) {
    var subterm = c1 * temp / (c2 + temp) + Math.log(rh/100);
    var dew_numer = c2 * subterm
    var dew_denom = c1 - subterm
    return dew_numer/dew_denom;
}

function compute_rh(dew, temp) {
    function conv(x) {
        return Math.exp((x*c1) / (x+c2));
    }
    return 100 * conv(dew) / conv(temp);
}

function compute_temp(rh, dew) {
    var subterm = c1 * dew / (c2 + dew) - Math.log(rh/100);
    var temp_numer = c2 * subterm;
    var temp_denom = c1 - subterm;
    return temp_numer / temp_denom;
}
