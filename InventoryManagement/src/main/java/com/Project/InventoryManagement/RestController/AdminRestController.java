package com.Project.InventoryManagement.RestController;

import org.springframework.beans.factory.annotation.Autowired;

import com.Project.InventoryManagement.Service.InventoryService;

public class AdminRestController extends EmployeeRestController{
    @Autowired
    public EmployeeRestController(InventoryService inventoryService){
        super(inventoryService);
    }
}
