// http://stackoverflow.com/questions/7137860/javascript-namespace-declaration-with-function-prototype

var tau = 2 * Math.PI;
var quarter_tau = Math.PI / 2;
var half_tau = Math.PI;

var SimpleBrush = (function () {
	/* circular brush */
	/** class Constructor **/
	var obj = function () {
		this.prev = null;
	};
	
	/** class methods **/
	obj.prototype = {
		drawTo: function (ctx, x, y, radius) {
			if (this.prev !== null) {
				var prev_radius = this.prev.radius;
				console.log("prev_radius:"+prev_radius);
				console.log("radius:"+radius);
				let modulus = Math.sqrt(Math.pow(x - this.prev.x, 2) + Math.pow(y - this.prev.y, 2));
				if (Math.max(radius, prev_radius) < modulus) {
					// alpha: angle between the two centers and the tangent
					let alpha = Math.acos((radius - prev_radius) / modulus);
					console.log("alpha:"+(360*alpha/tau));
					let theta = Math.atan2(x - this.prev.x, y - this.prev.y);
					console.log("theta:"+(360*theta/tau));
					ctx.beginPath();
					var x0 = prev_radius * Math.cos(theta + alpha) + this.prev.x;
					var y0 = prev_radius * Math.sin(theta + alpha) + this.prev.y;
					console.log("moveTo("+x0+", "+y0+")");
					ctx.moveTo(x0, y0);
					var x1 = radius * Math.cos(theta - quarter_tau - alpha) + x;
					var y1 = radius * Math.sin(theta - quarter_tau - alpha) + y;
					console.log("lineTo("+x1+", "+y1+")");
					var x2 = radius * Math.cos(theta + quarter_tau + alpha) + x;
					var y2 = radius * Math.sin(theta + quarter_tau + alpha) + y;
					console.log("arcTo("+x2+", "+y2+")");
					ctx.arcTo(x1, y1, x2, y2, radius);
					a = prev_radius * Math.cos(theta - alpha) + this.prev.x;
					b = prev_radius * Math.sin(theta - alpha) + this.prev.y;
					//console.log("lineTo("+a+", "+b+")");
					//ctx.lineTo(100, 0);
					//ctx.closePath();
				}
			} else {
				ctx.arc(x, y, radius, 0.0, tau, false);
			}

			ctx.stroke();
			this.prev = {
				x: x,
				y: y,
				radius: radius
			};
		}
	}
	return obj;
})();

