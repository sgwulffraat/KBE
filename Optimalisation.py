import numpy as np
immport scipy as sp
import random
import math

def COMPUTEROTATEDPLACEMENT(sheet, part,rotations):
    #Compute the candidate placements for each rotation
    local candidate_placements = empty list
    for each rotation in rotations do
        part.rotation = rotation
        local best_position = ComputePlacement(sheet, part)
        if best_position then candidate_placements.push((best_position, rotation))
    #If the part fits nowhere, fail the packing
    if candidate_placements is empty then return false
    #Select the best position and rotation among the candidates
    local best_position
    local best_rotation
    local best_score = ∞
    for each (position, rotation) in candidate_placements do
        part.position = position
        part.rotation = rotation
        score = SCORESHEET(sheet)
        if score ≤ best_score then
            best_position = position
            best_rotation = rotation
            best_score = score
    part.position = best_position
    part.rotation = best_rotation
    return sheet

def optimizebracket(sheets, parts, rotations):
    #Sort the parts in decreasing order of bounding box area
    parts.sort(part => -AREA(BBOX(part)))
    local used_sheets = empty list
    local failed_parts = empty list
    for part in parts do
        local part_placed = false
        for sheet in sheets do
            local best_placement = COMPUTEROTATEDPLACEMENT(sheet, part, rotations)
            #If the part fits nowhere, go to the next sheet
            if best_placement is false then
                continue
            #Once the part is placed, break out of the loop
            part_placed = true
            break
    #If all the sheets have been checked, the part does not fit
        if part_placed is false then failed_parts.push(part)
    for sheet in sheets do
        if sheet.parts is not empty then
            used_sheets.push(sheet)
    return used_sheets, failed_parts

