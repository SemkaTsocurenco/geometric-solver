# constraint_solver.py
import math
import time
import numpy as np

class ConstraintType:
    DISTANCE = "distance"
    PERPENDICULAR = "perpendicular"
    PARALLEL = "parallel"
    POINT_ON_LINE = "point_on_line"
    ANGLE = "angle"
    STATIONARY = "stationary"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class ConstraintSolver:
    def __init__(self, points):
        self.points = points
        self.constraints = []
        self.confirmation_callback = None
        self.lines = None

    def set_confirmation_callback(self, callback):
        self.confirmation_callback = callback

    def check_conflict(self, ctype, objs, val=None):
        for c in self.constraints:
            if c["type"] == ConstraintType.HORIZONTAL and ctype == ConstraintType.VERTICAL and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.VERTICAL and ctype == ConstraintType.HORIZONTAL and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.PARALLEL and ctype == ConstraintType.PERPENDICULAR and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.PERPENDICULAR and ctype == ConstraintType.PARALLEL and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.PARALLEL and ctype == ConstraintType.ANGLE and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.PERPENDICULAR and ctype == ConstraintType.ANGLE and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.HORIZONTAL and ctype == ConstraintType.ANGLE and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.VERTICAL and ctype == ConstraintType.ANGLE and c["objects"] == objs:
                return False
            if ctype == ConstraintType.ANGLE and c["type"] == ConstraintType.ANGLE and c["objects"] == objs:
                return False
            if c["type"] == ConstraintType.DISTANCE and ctype == ConstraintType.DISTANCE and c["objects"] == objs:
                return True
            if c["type"] == ConstraintType.DISTANCE and ctype == ConstraintType.DISTANCE and c["objects"] == objs:
                return True
            if c["type"] == ConstraintType.POINT_ON_LINE and ctype == ConstraintType.POINT_ON_LINE and c["objects"] == objs:
                return False
        return True

    def replace_distance_constraint(self, objs, distance):
        new_constraints = []
        replaced = False
        for c in self.constraints:
            if c["type"] == ConstraintType.DISTANCE and c["objects"] == objs:
                new_constraints.append({"type": ConstraintType.DISTANCE, "objects": objs, "value": distance})
                replaced = True
            else:
                new_constraints.append(c)
        self.constraints = new_constraints
        return replaced

    def add_distance_constraint(self, p1, p2, distance, replace=False):
        if p1 not in self.points or p2 not in self.points:
            return False
        objs = tuple(sorted([p1,p2]))
        if replace:
            if self.replace_distance_constraint(objs, distance):
                return True
        if not self.check_conflict(ConstraintType.DISTANCE, objs):
            # If same pair, replace anyway
            found = False
            for c in self.constraints:
                if c["type"] == ConstraintType.DISTANCE and c["objects"] == objs:
                    found = True
                    break
            if found:
                return self.replace_distance_constraint(objs, distance)
            return False
        self.constraints.append({
            "type": ConstraintType.DISTANCE,
            "objects": objs,
            "value": distance
        })
        return True

    def add_perpendicular_constraint(self, line1_idx, line2_idx):
        if self.lines is None or line1_idx<0 or line1_idx>=len(self.lines) or line2_idx<0 or line2_idx>=len(self.lines):
            return False
        objs = tuple(sorted([line1_idx,line2_idx]))
        if not self.check_conflict(ConstraintType.PERPENDICULAR, objs):
            return False
        self.constraints.append({
            "type": ConstraintType.PERPENDICULAR,
            "objects": objs,
        })
        return True

    def add_parallel_constraint(self, line1_idx, line2_idx):
        if self.lines is None or line1_idx<0 or line1_idx>=len(self.lines) or line2_idx<0 or line2_idx>=len(self.lines):
            return False
        objs = tuple(sorted([line1_idx,line2_idx]))
        if not self.check_conflict(ConstraintType.PARALLEL, objs):
            return False
        self.constraints.append({
            "type": ConstraintType.PARALLEL,
            "objects": objs,
        })
        return True

    def add_point_on_line_constraint(self, p, line_idx):
        if p not in self.points or self.lines is None or line_idx<0 or line_idx>=len(self.lines):
            return False
        objs = (p,line_idx)
        if not self.check_conflict(ConstraintType.POINT_ON_LINE, objs):
            return False
        self.constraints.append({
            "type": ConstraintType.POINT_ON_LINE,
            "objects": objs,
        })
        return True

    def add_angle_constraint(self, line1_idx, line2_idx, angle_degrees):
        if self.lines is None or line1_idx<0 or line1_idx>=len(self.lines) or line2_idx<0 or line2_idx>=len(self.lines):
            return False
        objs = tuple(sorted([line1_idx,line2_idx]))
        if not self.check_conflict(ConstraintType.ANGLE, objs, angle_degrees):
            return False
        self.constraints.append({
            "type": ConstraintType.ANGLE,
            "objects": objs,
            "value": angle_degrees
        })
        return True

    def add_stationary_constraint(self, p):
        if p not in self.points:
            return False
        objs = (p,)
        if not self.check_conflict(ConstraintType.STATIONARY, objs):
            return False
        self.constraints.append({
            "type": ConstraintType.STATIONARY,
            "objects": objs,
        })
        return True

    def add_horizontal_constraint(self, line_idx):
        if self.lines is None or line_idx<0 or line_idx>=len(self.lines):
            return False
        objs = (line_idx,)
        if not self.check_conflict(ConstraintType.HORIZONTAL, objs):
            return False
        # Remove vertical if exists
        self.constraints = [c for c in self.constraints if not (c["type"]==ConstraintType.VERTICAL and c["objects"]==objs)]
        self.constraints.append({
            "type": ConstraintType.HORIZONTAL,
            "objects": objs,
        })
        return True

    def add_vertical_constraint(self, line_idx):
        if self.lines is None or line_idx<0 or line_idx>=len(self.lines):
            return False
        objs = (line_idx,)
        if not self.check_conflict(ConstraintType.VERTICAL, objs):
            return False
        # Remove horizontal if exists
        self.constraints = [c for c in self.constraints if not (c["type"]==ConstraintType.HORIZONTAL and c["objects"]==objs)]
        self.constraints.append({
            "type": ConstraintType.VERTICAL,
            "objects": objs,
        })
        return True

    def on_point_delete(self, point_id):
        involved = [c for c in self.constraints if point_id in c["objects"] and c["type"]!=ConstraintType.STATIONARY]
        if not involved:
            self.constraints = [c for c in self.constraints if point_id not in c["objects"]]
            return True
        msg = f"Point {point_id} is involved in a constraint. Delete?"
        if self.confirmation_callback is not None:
            confirm = self.confirmation_callback(msg)
        else:
            confirm = True
        if confirm:
            self.constraints = [c for c in self.constraints if point_id not in c["objects"]]
            return True
        else:
            return False

    def get_constraints_info(self):
        return self.constraints

    def remove_all_constraints(self):
        self.constraints = []

    def is_stationary(self, point_id):
        for c in self.constraints:
            if c["type"] == ConstraintType.STATIONARY and point_id in c["objects"]:
                return True
        return False

    def set_lines_reference(self, lines):
        self.lines = lines

    def solve_constraints(self, iterations=20, tolerance=1e-3, learning_rate=0.1, max_time=3.0):
        if not self.constraints or self.lines is None:
            return True,0.0
        start_time = time.time()

        def move_point(pid, dx, dy, err):
            if pid in self.points and not self.is_stationary(pid):
                x,y = self.points[pid]
                f = 1.0
                if abs(err)<tolerance*10:
                    f=2.0
                if abs(err)<tolerance*5:
                    f=5.0
                if abs(err)<tolerance*2:
                    f=10.0
                self.points[pid] = (x+dx*f, y+dy*f)

        def line_vector(line_idx):
            p1_id, p2_id = self.lines[line_idx]
            x1,y1 = self.points[p1_id]
            x2,y2 = self.points[p2_id]
            return (x2 - x1, y2 - y1, p1_id, p2_id)

        max_error = 0.0
        for _ in range(iterations):
            if time.time()-start_time>max_time:
                return False,max_error
            max_error = 0.0
            for c in self.constraints:
                ctype = c["type"]
                objs = c["objects"]
                val = c.get("value", None)
                if ctype == ConstraintType.STATIONARY:
                    continue
                if ctype == ConstraintType.DISTANCE:
                    p1, p2 = objs
                    if p1 not in self.points or p2 not in self.points:
                        continue
                    x1,y1 = self.points[p1]
                    x2,y2 = self.points[p2]
                    dist = math.hypot(x2 - x1, y2 - y1)
                    target = val
                    error = dist - target
                    max_error = max(max_error, abs(error))
                    if abs(error) > tolerance and dist > 1e-9:
                        dx = (x2 - x1)/dist
                        dy = (y2 - y1)/dist
                        delta = error*0.5*learning_rate
                        if not self.is_stationary(p1):
                            move_point(p1, dx*delta, dy*delta, error)
                        if not self.is_stationary(p2):
                            move_point(p2, -dx*delta, -dy*delta, error)
                elif ctype in [ConstraintType.PERPENDICULAR, ConstraintType.PARALLEL, ConstraintType.ANGLE, ConstraintType.HORIZONTAL, ConstraintType.VERTICAL, ConstraintType.POINT_ON_LINE]:
                    if self.lines is None:
                        continue
                    if ctype == ConstraintType.POINT_ON_LINE:
                        p, line_idx = objs
                        if p not in self.points or line_idx<0 or line_idx>=len(self.lines):
                            continue
                        p1_id, p2_id = self.lines[line_idx]
                        if p1_id not in self.points or p2_id not in self.points:
                            continue
                        x0,y0 = self.points[p]
                        x1,y1 = self.points[p1_id]
                        x2,y2 = self.points[p2_id]
                        A = np.array([x1,y1])
                        B = np.array([x2,y2])
                        P = np.array([x0,y0])
                        AB = B - A
                        AP = P - A
                        denom = np.dot(AB,AB)
                        if denom<1e-9:
                            continue
                        t = np.dot(AP, AB)/denom
                        Pp = A + t*AB
                        dx = Pp[0]-x0
                        dy = Pp[1]-y0
                        dist = math.hypot(dx,dy)
                        error = dist
                        max_error = max(max_error, abs(error))
                        if error>tolerance:
                            step = error*learning_rate
                            if not self.is_stationary(p):
                                move_point(p, dx*learning_rate, dy*learning_rate,error)
                            else:
                                move_point(p1_id, dx*step*0.5, dy*step*0.5,error)
                                move_point(p2_id, dx*step*0.5, dy*step*0.5,error)
                    else:
                        if ctype in [ConstraintType.HORIZONTAL, ConstraintType.VERTICAL]:
                            line1 = objs[0]
                            if line1<0 or line1>=len(self.lines):
                                continue
                            vx, vy, p1a, p1b = line_vector(line1)
                            len1 = math.hypot(vx, vy)
                            if len1<1e-9:
                                continue
                            nx1, ny1 = vx/len1, vy/len1
                            if ctype == ConstraintType.HORIZONTAL:
                                error = ny1
                                max_error = max(max_error, abs(error))
                                if abs(error)>tolerance:
                                    step = error*learning_rate
                                    dist = len1
                                    sign = 1.0
                                    if error>0:
                                        sign=1.0
                                    else:
                                        sign=-1.0
                                    move_point(p1b, -ny1*step*dist, nx1*step*dist, error)
                            else:
                                error = nx1
                                max_error = max(max_error, abs(error))
                                if abs(error)>tolerance:
                                    step = error*learning_rate
                                    dist = len1
                                    sign = 1.0
                                    if error>0:
                                        sign=1.0
                                    else:
                                        sign=-1.0
                                    move_point(p1b, -ny1*step*dist, nx1*step*dist, error)
                        else:
                            line1, line2 = objs
                            if line1<0 or line1>=len(self.lines) or line2<0 or line2>=len(self.lines):
                                continue
                            vx1, vy1, p1a, p1b = line_vector(line1)
                            vx2, vy2, p2a, p2b = line_vector(line2)
                            len1 = math.hypot(vx1, vy1)
                            len2 = math.hypot(vx2, vy2)
                            if len1 < 1e-9 or len2 < 1e-9:
                                continue
                            nx1, ny1 = vx1/len1, vy1/len1
                            nx2, ny2 = vx2/len2, vy2/len2
                            if ctype == ConstraintType.PERPENDICULAR:
                                dot = nx1*nx2 + ny1*ny2
                                error = dot
                                max_error = max(max_error, abs(error))
                                if abs(error)>tolerance:
                                    step = error*learning_rate
                                    dist = len1
                                    move_point(p1b, -ny2*step*dist, nx2*step*dist, error)
                            elif ctype == ConstraintType.PARALLEL:
                                cross = nx1*ny2 - ny1*nx2
                                error = cross
                                max_error = max(max_error, abs(error))
                                if abs(error)>tolerance:
                                    step = error*learning_rate
                                    dist = len1
                                    move_point(p1b, -ny1*step*dist, nx1*step*dist, error)
                            elif ctype == ConstraintType.ANGLE:
                                desired_angle_deg = val
                                desired_angle = math.radians(desired_angle_deg)
                                dot = nx1*nx2 + ny1*ny2
                                if dot>1:dot=1
                                if dot<-1:dot=-1
                                current_angle = math.acos(dot)
                                d_angle = current_angle - desired_angle
                                # choose shortest rotation direction
                                if d_angle>math.pi:
                                    d_angle-=2*math.pi
                                if d_angle<-math.pi:
                                    d_angle+=2*math.pi
                                error = d_angle
                                max_error = max(max_error, abs(error))
                                if abs(error)>tolerance:
                                    step = error*learning_rate
                                    dist = len1
                                    move_point(p1b, -ny1*step*dist, nx1*step*dist, error)

            if max_error < tolerance:
                return True,max_error
        return False,max_error
