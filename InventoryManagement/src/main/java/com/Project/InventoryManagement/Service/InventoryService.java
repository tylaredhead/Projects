package com.Project.InventoryManagement.Service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.Project.InventoryManagement.Entity.*;
import com.Project.InventoryManagement.Repository.*;


@Service
public class InventoryService implements InventoryServiceInterface{
    private final StockRepository stockRepo;
    private final SupplierRepository supplierRepo;
    private final ProductRepository productRepo;

    @Autowired
    public InventoryService(StockRepository stockRepo, 
                            SupplierRepository supplierRepo, 
                            ProductRepository productRepo){

        this.stockRepo = stockRepo;
        this.supplierRepo = supplierRepo;
        this.productRepo = productRepo;
    }

    @Override
    public Stock saveStock(Stock stock){
        return stockRepo.save(stock);
    }
    
    @Override
    public List<Stock> getAllStock(){
        return stockRepo.findAll();
    }
   
    @Override
    public Stock findById(int id){
        return stockRepo.findById(id);
    }

    @Override
    public List<Stock> findStockByProductName(String name){
        return stockRepo.findStockByProductName(name);
    }
   
    @Override
    public List<Stock> findByRating(String rating){
        return stockRepo.findByRating(rating);
    }

    @Override
    public List<Stock> findByQuantity(int quantity){
        return stockRepo.findByQuantity(quantity);
    }

    @Override
    public Stock updateRating(int id, String rating){
        Stock stock = stockRepo.findById(id);
        stock.setRating(rating);
        return stockRepo.save(stock);
    }

    @Override
    public Stock updateQuantity(int id, int quantity){
        Stock stock = stockRepo.findById(id);
        stock.setQuantity(stock.getQuantity() + quantity);
        return stockRepo.save(stock);
    }

    @Override
    public void deleteById(int id){
        stockRepo.deleteById(id);
    }

    @Override
    public Supplier saveSupplier(Supplier supplier){
        return supplierRepo.save(supplier);
    }

    @Override
    public List<Supplier> getAllSuppliers(){
        return supplierRepo.findAll();
    }

    @Override
    public Supplier findBySupplierId(int id){
        return supplierRepo.findById(id);
    }

    @Override
    public List<Supplier> findBySupplierName(String name){
        return supplierRepo.findBySupplierName(name);
    }

    @Override
    public List<Supplier> findBySupplierNo(String no){
        return supplierRepo.findBySupplierNo(no);
    }

    @Override
    public List<Supplier> findBySupplierEmail(String email){
        return supplierRepo.findBySupplierEmail(email);
    }

    @Override
    public Supplier updateSupplierName(int id, String name){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierName(name);
        return supplierRepo.save(supplier);
    }

    @Override
    public Supplier updateSupplierNo(int id, String no){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierNo(no);
        return supplierRepo.save(supplier);
    }

    @Override
    public Supplier updateSupplierEmail(int id, String email){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierEmail(email);
        return supplierRepo.save(supplier);
    }

    @Override
    public void deleteBySupplierId(int id){
        supplierRepo.deleteById(id);
    }

    @Override
    public void deleteBySupplierName(String name){
        supplierRepo.deleteBySupplierName(name);
    }

    @Override
    public Product saveProduct(Product product){
        return productRepo.save(product);
    }

    @Override
    public List<Product> getAllProducts(){
        return productRepo.findAll();
    }

    @Override
    public Product findByProductId(int id){
        return productRepo.findById(id);
    }

    @Override
    public List<Product> findByProductName(String name){
        return productRepo.findByProductName(name);
    }

    @Override
    public List<Product> findByProductDesc(String desc){
        return productRepo.findByProductDesc(desc);
    }

    @Override
    public List<Product> findByProductType(String type){
        return productRepo.findByProductType(type);
    }

    @Override
    public List<Product> findByPrice(float price){
        return productRepo.findByPrice(price);
    }

    @Override 
    public List<Product> findProductBySupplierName(String name){
        return productRepo.findProductBySupplierName(name);
    }


    @Override
    public Product updateProductName(int id, String name){
        Product product = productRepo.findById(id);
        product.setProductName(name);
        return productRepo.save(product);
    }

    @Override
    public Product updateProductDesc(int id, String desc){
        Product product = productRepo.findById(id);
        product.setProductDesc(desc);
        return productRepo.save(product);
    }

    @Override
    public Product updateProductType(int id, String type){
        Product product = productRepo.findById(id);
        product.setProductType(type);
        return productRepo.save(product);
    }

    @Override
    public Product updatePrice(int id, float price){
        Product product = productRepo.findById(id);
        product.setPrice(price);
        return productRepo.save(product);
    }

    @Override
    public void deleteByProductId(int id){
        productRepo.deleteById(id);
    }

    @Override
    public void deleteByProductName(String name){
        productRepo.deleteByProductName(name);
    }
}