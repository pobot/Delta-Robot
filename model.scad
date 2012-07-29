mdf =6;

module vwheels(){

	module vwheel(){
		color([0.6,0.6,0.6]){
			rotate_extrude(file = "vwheel.dxf", layer = "bearing",convexity = 10);
		}
		color([0.5,0.5,0.5]){
			for(i =[0:10]){
				rotate([0,0,360/10 *i])translate([5.2,0,-3])sphere(r=1.8,$fn = 20);
				rotate([0,0,360/10 *i])translate([5.2,0,3])sphere(r=1.8,$fn = 20);
			}
		}
		color([0.4,0.4,0.4]){
			rotate_extrude(file = "vwheel.dxf", layer = "washer",convexity = 10);
		}
		color([0.1,0.1,0.1]){
			rotate_extrude(file = "vwheel.dxf", layer = "v_wheel",convexity = 10);
		}
	}
	
	
	module washer(){
		color([0.4,0.4,0.4]){
			rotate_extrude(file = "vwheel.dxf", layer = "washer",convexity = 10);
		}
	}

	translate([0,20,0]){
		rotate([90,90,0]){
			translate([-0,-32,0]){
				vwheel();
				translate([0,0,-5.5])washer();
			}
		
			translate([-20,32,0]){
				vwheel();
				translate([0,0,-5.5])washer();
			}
			translate([20,32,0]){
				vwheel();
				translate([0,0,-5.5])washer();
			}
		}
	}
}

module makerslide(length) {
	color([0.5,0.5,0.5]){
		linear_extrude(file = "makerslide.dxf", layer = "makerslide",height =length,convexity = 10);
	}
}


module carrige(){
	rotate([90,0,0]){
		translate([0,0,-36]){
			linear_extrude(file = "parts.dxf", layer = "carrige_base",height = mdf,	convexity = 10);
		}	

	}

	rotate([0,90,0]){
		translate([0,36,20]){
			color([0.4,0.4,0.7])linear_extrude(file = "parts.dxf", layer = "carrige_side",height = mdf,	convexity = 10);
		}	
		translate([0,36,-26]){
			color([0.4,0.4,0.7])linear_extrude(file = "parts.dxf", layer = "carrige_side",height = mdf,	convexity = 10);
		}	

	}

	translate([0,36,-30]){
		color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "carrige_nut_stop",height = mdf	,convexity = 10);
	}
	translate([0,36,-24]){
		color([0.7,0.4,0.4])linear_extrude(file = "parts.dxf", layer = "carrige_nut_holder",height = mdf	,convexity = 10);
	}
	translate([0,36,-18]){
		color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "carrige_nut_stop",height = mdf	,convexity = 10);
	}
	translate([0,36,24]){
		color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "carrige_nut_stop",height = mdf,convexity = 10);
	}
	translate([0,36,18]){
		color([0.7,0.4,0.4])linear_extrude(file = "parts.dxf", layer = "carrige_nut_holder",height = mdf	,convexity = 10);
	}
	translate([0,36,12]){
		color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "carrige_nut_stop",height = mdf,convexity = 10);
	}
	vwheels();
}

module head(){
	color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "head_base",height = mdf,convexity = 10);
	translate([0,0,26]){
		color([0.4,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "head_base",height = mdf,convexity = 10);
	}
	translate([0,0,32]){
		color([0.7,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "head_plate",height = mdf,convexity = 10);
	}
	translate([0,0,-6]){
		color([0.7,0.7,0.4,0.8])linear_extrude(file = "parts.dxf", layer = "head_plate",height = mdf,convexity = 10);
	}
	for(r=[0,120,240]){
		rotate([0,0,r]){
			translate([20,20,6])rotate([90,0,0])rotate([0,90,0]){
				color([0.4,0.7,0.7,0.8])linear_extrude(file = "parts.dxf", layer = "head_arm",height = mdf,convexity = 10);
	}
			translate([-26,20,6])rotate([90,0,0])rotate([0,90,0]){
				color([0.4,0.7,0.7,0.8])linear_extrude(file = "parts.dxf", layer = "head_arm",height = mdf,convexity = 10);
			}
		}
	}

}

module body(){
	color([0.4,0.7,0.7,0.8])linear_extrude(file = "parts.dxf", layer = "body_base",height = mdf,convexity = 10);
	color([0.4,0.7,0.7,0.8])translate([0,0,406])linear_extrude(file = "parts.dxf", layer = "body_top",height = mdf,convexity = 10);

	for(r=[0,120,240]){
		rotate([0,0,r]){
			color([0.7,0.7,0.4,0.8])translate([3,70,0])rotate([-90,0,90])linear_extrude(file = "parts.dxf", layer = "body_spine",height = mdf,convexity = 10);
			color([0.7,0.4,0.7,0.8])translate([0,200,0])rotate([-90,0,0])linear_extrude(file = "parts.dxf", layer = "body_feet",height = mdf,convexity = 10);
			translate([0,0,400])linear_extrude(file = "parts.dxf", layer = "body_bearing_stop",height = mdf,convexity = 10);
			translate([0,0,412])linear_extrude(file = "parts.dxf", layer = "body_bearing_stop",height = mdf,convexity = 10);	
			translate([0,0,432])linear_extrude(file = "parts.dxf", layer = "body_motor_mount",height = mdf,convexity = 10);	
		}
	}
}

module screws(){
	for(r=[0,120,240]){
		rotate([0,0,r]){
			translate([0,154,260])cylinder(h = 300, r = 3, center = true);
		}
	}
}


screws();

translate([0,0,-6])body();

translate([0,0,46])head();

feet();

for(r=[0,120,240]){
	rotate([0,0,r]){
		translate([0,200,0])rotate([0,0,180]){
			makerslide(400);
			translate([0,0,266])carrige();
		}
	}
}